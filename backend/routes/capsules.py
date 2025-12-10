from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.supabase_client import supabase
from utils.email_sender import send_capsule_email, send_capsule_opened_email

capsules_bp = Blueprint('capsules', __name__)


@capsules_bp.route('', methods=['POST'])
def create_capsule():
    """
    Create a new time capsule
    """
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['creator_email', 'title', 'message', 'open_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Insert capsule into database
        capsule_data = {
            'creator_email': data['creator_email'],
            'title': data['title'],
            'message': data['message'],
            'media_url': data.get('media_url', None),
            'open_date': data['open_date'],
            'is_opened': False,
            'notification_sent': False,
            'created_at': datetime.utcnow().isoformat()
        }

        result = supabase.table('time_capsules').insert(capsule_data).execute()

        if not result.data:
            return jsonify({'error': 'Failed to create capsule'}), 500

        capsule_id = result.data[0]['id']

        # Send confirmation email
        view_link = f'http://localhost:3000/view-capsule.html?id={capsule_id}'
        email_data = {
            'title': data['title'],
            'open_date': data['open_date'],
            'view_link': view_link
        }

        send_capsule_email(data['creator_email'], email_data)

        return jsonify({
            'success': True,
            'capsule_id': capsule_id,
            'message': 'Zaman kapsülünüz başarıyla oluşturuldu!'
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@capsules_bp.route('/<capsule_id>', methods=['GET'])
def get_capsule(capsule_id):
    """
    Get capsule details by ID (supports both UUID and integer)
    Also sends opening notification email if time has arrived and not sent yet
    """
    try:
        result = supabase.table('time_capsules').select('*').eq('id', capsule_id).execute()

        if not result.data:
            return jsonify({'error': 'Capsule not found'}), 404

        capsule = result.data[0]
        
        # Check if opening time has arrived and send email if needed
        open_date = datetime.fromisoformat(capsule['open_date'].replace('Z', '+00:00'))
        current_date = datetime.now(timezone.utc)
        
        if current_date >= open_date and not capsule.get('is_opened', False) and not capsule.get('notification_sent', False):
            view_link = f'http://localhost:3000/view-capsule.html?id={capsule_id}'
            email_data = {
                'title': capsule['title'],
                'view_link': view_link
            }
            
            if send_capsule_opened_email(capsule['creator_email'], email_data):
                # Mark as email sent
                supabase.table('time_capsules').update({'notification_sent': True}).eq('id', capsule_id).execute()
                # Refresh capsule data
                result = supabase.table('time_capsules').select('*').eq('id', capsule_id).execute()
                if result.data:
                    capsule = result.data[0]

        return jsonify(capsule), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@capsules_bp.route('/check/<capsule_id>', methods=['GET'])
def check_capsule(capsule_id):
    """
    Check if capsule can be opened (supports both UUID and integer)
    Also sends opening notification email if time has arrived and not sent yet
    """
    try:
        result = supabase.table('time_capsules').select('*').eq('id', capsule_id).execute()

        if not result.data:
            return jsonify({'error': 'Capsule not found'}), 404

        capsule = result.data[0]
        open_date = datetime.fromisoformat(capsule['open_date'].replace('Z', '+00:00'))
        current_date = datetime.now(timezone.utc)

        can_open = current_date >= open_date

        # Send opening notification email if time has arrived and not sent yet
        if can_open and not capsule.get('is_opened', False) and not capsule.get('notification_sent', False):
            view_link = f'http://localhost:3000/view-capsule.html?id={capsule_id}'
            email_data = {
                'title': capsule['title'],
                'view_link': view_link
            }
            
            if send_capsule_opened_email(capsule['creator_email'], email_data):
                # Mark as email sent
                supabase.table('time_capsules').update({'notification_sent': True}).eq('id', capsule_id).execute()

        return jsonify({
            'can_open': can_open,
            'open_date': capsule['open_date'],
            'is_opened': capsule['is_opened']
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@capsules_bp.route('/<capsule_id>/open', methods=['PUT'])
def open_capsule(capsule_id):
    """
    Mark capsule as opened (supports both UUID and integer)
    """
    try:
        # First check if it can be opened
        result = supabase.table('time_capsules').select('*').eq('id', capsule_id).execute()

        if not result.data:
            return jsonify({'error': 'Capsule not found'}), 404

        capsule = result.data[0]
        open_date = datetime.fromisoformat(capsule['open_date'].replace('Z', '+00:00'))
        current_date = datetime.now(timezone.utc)

        if current_date < open_date:
            return jsonify({'error': 'Capsule cannot be opened yet'}), 403

        # Mark as opened
        result = supabase.table('time_capsules').update({'is_opened': True}).eq('id', capsule_id).execute()

        if not result.data:
            return jsonify({'error': 'Failed to open capsule'}), 500

        return jsonify({'success': True}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@capsules_bp.route('/check-and-send-emails', methods=['POST'])
def check_and_send_opening_emails():
    """
    Check for capsules that are ready to open and send notification emails
    This endpoint should be called periodically (e.g., via cron job)
    """
    try:
        current_date = datetime.now(timezone.utc)
        
        # Find capsules that:
        # 1. Have not had notification_sent yet
        # 2. Are not yet opened
        result = supabase.table('time_capsules').select('*').eq('notification_sent', False).eq('is_opened', False).execute()
        
        if not result.data:
            return jsonify({
                'success': True,
                'message': 'No capsules ready for opening',
                'checked': 0
            }), 200
        
        sent_count = 0
        for capsule in result.data:
            open_date = datetime.fromisoformat(capsule['open_date'].replace('Z', '+00:00'))
            
            # Check if opening time has arrived
            if current_date >= open_date:
                view_link = f'http://localhost:3000/view-capsule.html?id={capsule["id"]}'
                email_data = {
                    'title': capsule['title'],
                    'view_link': view_link
                }
                
                # Send email
                if send_capsule_opened_email(capsule['creator_email'], email_data):
                    # Mark as email sent
                    supabase.table('time_capsules').update({'notification_sent': True}).eq('id', capsule['id']).execute()
                    sent_count += 1
        
        return jsonify({
            'success': True,
            'message': f'Sent {sent_count} opening notification email(s)',
            'sent': sent_count
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
