from flask import Blueprint, request, jsonify
from datetime import datetime
import sys
import os
import random

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.supabase_client import supabase

music_bp = Blueprint('music', __name__)


@music_bp.route('/jars', methods=['GET'])
def get_jar_types():
    """
    Get all jar types
    """
    try:
        result = supabase.table('jar_types').select('*').execute()

        if not result.data:
            return jsonify([]), 200

        return jsonify(result.data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@music_bp.route('', methods=['POST'])
def add_music():
    """
    Add a new music to a jar
    """
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['jar_type', 'song_name', 'artist_name', 'youtube_url', 'added_by']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Insert music into database
        music_data = {
            'jar_type': data['jar_type'],
            'song_name': data['song_name'],
            'artist_name': data['artist_name'],
            'youtube_url': data['youtube_url'],
            'added_by': data['added_by'],
            'play_count': 0,
            'created_at': datetime.utcnow().isoformat()
        }

        result = supabase.table('music_jars').insert(music_data).execute()

        if not result.data:
            return jsonify({'error': 'Failed to add music'}), 500

        return jsonify({
            'success': True,
            'music_id': result.data[0]['id'],
            'message': 'Müzik başarıyla eklendi!'
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@music_bp.route('/random', methods=['GET'])
def get_random_music_any():
    """
    Get a random music from any jar type
    """
    try:
        # Get all music from all jar types
        result = supabase.table('music_jars').select('*').execute()

        if not result.data or len(result.data) == 0:
            return jsonify({'error': 'No music found'}), 404

        # Select a random music
        random_music = random.choice(result.data)

        return jsonify(random_music), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@music_bp.route('/random/<jar_type>', methods=['GET'])
def get_random_music(jar_type):
    """
    Get a random music from a specific jar type
    """
    try:
        # Get all music from this jar type
        result = supabase.table('music_jars').select('*').eq('jar_type', jar_type).execute()

        if not result.data or len(result.data) == 0:
            return jsonify({'error': 'No music found in this jar'}), 404

        # Select a random music
        random_music = random.choice(result.data)

        return jsonify(random_music), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@music_bp.route('/<music_id>/play', methods=['PUT'])
def increment_play_count(music_id):
    """
    Increment play count for a music (supports both UUID and integer)
    """
    try:
        # First get current play count
        result = supabase.table('music_jars').select('play_count').eq('id', music_id).execute()

        if not result.data:
            return jsonify({'error': 'Music not found'}), 404

        current_count = result.data[0]['play_count']
        new_count = current_count + 1

        # Update play count
        result = supabase.table('music_jars').update({'play_count': new_count}).eq('id', music_id).execute()

        if not result.data:
            return jsonify({'error': 'Failed to update play count'}), 500

        return jsonify({
            'success': True,
            'play_count': new_count
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
