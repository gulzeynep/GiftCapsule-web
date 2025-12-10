from flask import Blueprint, request, jsonify
from datetime import datetime
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.supabase_client import supabase
from utils.email_sender import send_gift_email

gifts_bp = Blueprint('gifts', __name__)


@gifts_bp.route('', methods=['POST'])
def create_gift():
    """
    Create a new gift and send email notification
    """
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['sender_name', 'recipient_name', 'recipient_email', 'card_template', 'message']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Insert gift into database
        gift_data = {
            'sender_name': data['sender_name'],
            'recipient_name': data['recipient_name'],
            'recipient_email': data['recipient_email'],
            'card_template': data['card_template'],
            'message': data['message'],
            'is_viewed': False,
            'created_at': datetime.utcnow().isoformat()
        }

        result = supabase.table('gifts').insert(gift_data).execute()

        if not result.data:
            return jsonify({'error': 'Failed to create gift'}), 500

        gift_id = result.data[0]['id']

        # Send email notification
        view_link = f'http://localhost:3000/view-gift.html?id={gift_id}'
        email_data = {
            'sender_name': data['sender_name'],
            'recipient_name': data['recipient_name'],
            'view_link': view_link
        }

        send_gift_email(data['recipient_email'], email_data)

        return jsonify({
            'success': True,
            'gift_id': gift_id,
            'view_link': view_link
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@gifts_bp.route('/<gift_id>', methods=['GET'])
def get_gift(gift_id):
    """
    Get gift details by ID (supports both UUID and integer)
    """
    try:
        result = supabase.table('gifts').select('*').eq('id', gift_id).execute()

        if not result.data:
            return jsonify({'error': 'Gift not found'}), 404

        return jsonify(result.data[0]), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@gifts_bp.route('/<gift_id>/view', methods=['PUT'])
def mark_gift_viewed(gift_id):
    """
    Mark gift as viewed (supports both UUID and integer)
    """
    try:
        result = supabase.table('gifts').update({'is_viewed': True}).eq('id', gift_id).execute()

        if not result.data:
            return jsonify({'error': 'Gift not found'}), 404

        return jsonify({'success': True}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
