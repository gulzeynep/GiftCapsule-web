// Global variables
let jarTypes = [];
let currentJarType = null;
let currentMusicId = null;

// Load jar types on page load
window.addEventListener('DOMContentLoaded', () => {
    loadJarTypes();
});

// Load jar types from API
async function loadJarTypes() {
    try {
        const response = await fetch('http://localhost:5000/api/music/jars');

        if (!response.ok) {
            throw new Error('Failed to load jar types');
        }

        jarTypes = await response.json();

        // Render jar cards
        renderJarCards();

        // Populate jar type select in add music form
        populateJarTypeSelect();

    } catch (error) {
        console.error('Error loading jar types:', error);
        alert('Jar tipleri yüklenirken bir hata oluştu');
    }
}

// Render jar cards
function renderJarCards() {
    const container = document.getElementById('jarsContainer');
    container.innerHTML = '';

    jarTypes.forEach(jar => {
        const card = document.createElement('div');
        card.className = 'jar-card bg-white rounded-2xl shadow-xl p-4 md:p-6 text-center cursor-pointer';
        card.style.borderTop = `4px solid ${jar.color}`;
        card.onclick = () => selectJar(jar.name);

        card.innerHTML = `
            <div class="text-4xl md:text-5xl mb-2 md:mb-3">${jar.emoji}</div>
            <h3 class="text-lg md:text-xl font-bold text-gray-800 mb-1 md:mb-2">${jar.name}</h3>
            <p class="text-gray-600 text-xs md:text-sm">${jar.description}</p>
        `;

        container.appendChild(card);
    });
}

// Populate jar type select in add music form
function populateJarTypeSelect() {
    const select = document.getElementById('jar_type_select');
    select.innerHTML = '<option value="">Seçiniz...</option>';

    jarTypes.forEach(jar => {
        const option = document.createElement('option');
        option.value = jar.name;
        option.textContent = `${jar.emoji} ${jar.name}`;
        select.appendChild(option);
    });
}

// Select a jar and load random music
async function selectJar(jarType) {
    currentJarType = jarType;

    // Show loading state
    document.getElementById('loadingState').classList.remove('hidden');
    document.getElementById('playerSection').classList.add('hidden');

    try {
        const response = await fetch(`http://localhost:5000/api/music/random/${jarType}`);

        if (!response.ok) {
            throw new Error('Bu jar\'da henüz müzik bulunmuyor');
        }

        const music = await response.json();
        displayMusic(music);

    } catch (error) {
        document.getElementById('loadingState').classList.add('hidden');
        alert(error.message);
    }
}

// Display music in player
function displayMusic(music) {
    currentMusicId = music.id;
    
    // Update current jar type if music has jar_type
    if (music.jar_type) {
        currentJarType = music.jar_type;
    }

    // Hide loading, show player
    document.getElementById('loadingState').classList.add('hidden');
    document.getElementById('playerSection').classList.remove('hidden');

    // Update music info
    const jarTypeElement = document.getElementById('currentJarType');
    if (music.jar_type) {
        // Find jar emoji and name
        const jar = jarTypes.find(j => j.name === music.jar_type);
        if (jar) {
            jarTypeElement.textContent = `${jar.emoji} ${jar.name}`;
            jarTypeElement.classList.remove('hidden');
        } else {
            jarTypeElement.textContent = music.jar_type;
            jarTypeElement.classList.remove('hidden');
        }
    } else {
        jarTypeElement.classList.add('hidden');
    }
    
    document.getElementById('currentSong').textContent = music.song_name;
    document.getElementById('currentArtist').textContent = music.artist_name;
    document.getElementById('playCount').textContent = `${music.play_count} kez çalındı`;

    // Extract and validate YouTube video ID
    const videoId = extractYouTubeId(music.youtube_url);

    if (!videoId) {
        alert('Geçersiz YouTube URL. Lütfen geçerli bir YouTube linki olduğundan emin olun.');
        document.getElementById('loadingState').classList.add('hidden');
        return;
    }

    // Load YouTube player
    const playerContainer = document.getElementById('youtubePlayer');
    playerContainer.innerHTML = `
        <iframe width="100%" height="100%"
                src="https://www.youtube.com/embed/${videoId}?autoplay=1"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen>
        </iframe>
    `;

    // Increment play count
    incrementPlayCount(music.id);

    // Scroll to player
    document.getElementById('playerSection').scrollIntoView({ behavior: 'smooth' });
}

/**
 * Validates and extracts YouTube video ID from various URL formats
 * 
 * Supports:
 * - Standard: https://www.youtube.com/watch?v=VIDEO_ID
 * - Short: https://youtu.be/VIDEO_ID
 * - Embed: https://www.youtube.com/embed/VIDEO_ID
 * - Mobile: https://m.youtube.com/watch?v=VIDEO_ID
 * - With parameters: https://youtube.com/watch?v=VIDEO_ID&t=123s&list=...
 * - Direct ID: VIDEO_ID (11 characters)
 * 
 * @param {string} url - YouTube URL or video ID
 * @returns {string|null} - Valid YouTube video ID (11 characters) or null if invalid
 */
function extractYouTubeId(url) {
    if (!url || typeof url !== 'string') {
        return null;
    }

    // Trim whitespace
    url = url.trim();

    // YouTube video ID pattern: exactly 11 alphanumeric characters, underscore, or hyphen
    const VIDEO_ID_PATTERN = /^[a-zA-Z0-9_-]{11}$/;

    // If it's already a valid video ID, return it
    if (VIDEO_ID_PATTERN.test(url)) {
        return url;
    }

    // Try to extract video ID from various URL patterns
    const patterns = [
        // Standard watch URLs: youtube.com/watch?v=VIDEO_ID or youtu.be/VIDEO_ID
        /(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})/,
        // Embed URLs: youtube.com/embed/VIDEO_ID
        /youtube\.com\/embed\/([a-zA-Z0-9_-]{11})/,
        // Short URLs with parameters: youtu.be/VIDEO_ID?t=123
        /youtu\.be\/([a-zA-Z0-9_-]{11})(?:\?|$)/,
        // v/ format: youtube.com/v/VIDEO_ID
        /youtube\.com\/v\/([a-zA-Z0-9_-]{11})/,
        // Mobile URLs: m.youtube.com/watch?v=VIDEO_ID
        /m\.youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})/,
        // URL with &v= parameter (when v is not the first parameter)
        /[&?]v=([a-zA-Z0-9_-]{11})/,
    ];

    for (const pattern of patterns) {
        const match = url.match(pattern);
        if (match && match[1] && VIDEO_ID_PATTERN.test(match[1])) {
            return match[1];
        }
    }

    return null;
}

/**
 * Validates if a string is a valid YouTube URL or video ID
 * 
 * @param {string} url - YouTube URL or video ID to validate
 * @returns {boolean} - True if valid, false otherwise
 */
function isValidYouTubeUrl(url) {
    return extractYouTubeId(url) !== null;
}

// Get random music from any jar (general random)
async function getRandomMusicAny() {
    // Show loading state
    document.getElementById('loadingState').classList.remove('hidden');
    document.getElementById('playerSection').classList.add('hidden');

    // Reset current jar type since it's from any jar
    currentJarType = null;

    try {
        const response = await fetch('http://localhost:5000/api/music/random');

        if (!response.ok) {
            throw new Error('Henüz müzik bulunmuyor');
        }

        const music = await response.json();
        displayMusic(music);

    } catch (error) {
        document.getElementById('loadingState').classList.add('hidden');
        alert(error.message);
    }
}

// Get another random song from the same jar
function getAnotherSong() {
    if (currentJarType) {
        selectJar(currentJarType);
    } else {
        // If no specific jar type, get random from any jar
        getRandomMusicAny();
    }
}

// Increment play count
async function incrementPlayCount(musicId) {
    try {
        await fetch(`http://localhost:5000/api/music/${musicId}/play`, {
            method: 'PUT'
        });
    } catch (error) {
        console.error('Error incrementing play count:', error);
    }
}

// Toggle add music form
function toggleAddMusic() {
    const addSection = document.getElementById('addMusicSection');
    addSection.classList.toggle('hidden');

    if (!addSection.classList.contains('hidden')) {
        addSection.scrollIntoView({ behavior: 'smooth' });
    }
}

// Add music form handler
document.getElementById('addMusicForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = {
        jar_type: document.getElementById('jar_type_select').value,
        song_name: document.getElementById('song_name').value,
        artist_name: document.getElementById('artist_name').value,
        youtube_url: document.getElementById('youtube_url').value,
        added_by: document.getElementById('added_by').value || 'Anonim'
    };

    // Validate YouTube URL
    if (!isValidYouTubeUrl(formData.youtube_url)) {
        document.getElementById('addErrorText').textContent = 
            'Geçerli bir YouTube URL girin (örn: https://www.youtube.com/watch?v=VIDEO_ID veya https://youtu.be/VIDEO_ID)';
        document.getElementById('addErrorMessage').classList.remove('hidden');
        return;
    }

    // Disable submit button
    const submitBtn = document.getElementById('submitMusicBtn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Ekleniyor...';

    // Hide previous messages
    document.getElementById('addSuccessMessage').classList.add('hidden');
    document.getElementById('addErrorMessage').classList.add('hidden');

    try {
        const response = await fetch('http://localhost:5000/api/music', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Müzik eklenemedi');
        }

        // Show success message
        document.getElementById('addSuccessMessage').classList.remove('hidden');

        // Reset form
        document.getElementById('addMusicForm').reset();

        // Hide form after 2 seconds
        setTimeout(() => {
            toggleAddMusic();
            document.getElementById('addSuccessMessage').classList.add('hidden');
        }, 2000);

    } catch (error) {
        // Show error message
        document.getElementById('addErrorText').textContent = error.message;
        document.getElementById('addErrorMessage').classList.remove('hidden');
    } finally {
        // Re-enable submit button
        submitBtn.disabled = false;
        submitBtn.textContent = 'Müziği Ekle';
    }
});
