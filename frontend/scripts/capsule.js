// Global variable to store capsule link
let currentCapsuleLink = '';

// Capsule form handler
document.getElementById('capsuleForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    // Get form data
    const openDateInput = document.getElementById('open_date').value;
    const openDate = new Date(openDateInput);

    // Validate future date
    if (openDate <= new Date()) {
        document.getElementById('errorText').textContent = 'Açılış tarihi gelecekte bir tarih olmalıdır.';
        document.getElementById('errorMessage').classList.remove('hidden');
        return;
    }

    const formData = {
        creator_email: document.getElementById('creator_email').value,
        title: document.getElementById('title').value,
        message: document.getElementById('message').value,
        media_url: document.getElementById('media_url').value || null,
        open_date: openDate.toISOString()
    };

    // Disable submit button
    const submitBtn = document.getElementById('submitBtn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Oluşturuluyor...';

    // Hide previous messages
    document.getElementById('successMessage').classList.add('hidden');
    document.getElementById('errorMessage').classList.add('hidden');
    document.getElementById('copyCapsuleSuccess').classList.add('hidden');

    try {
        const response = await fetch('http://localhost:5000/api/capsules', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Kapsül oluşturulamadı');
        }

        // Create view link
        const capsuleLink = `http://localhost:3000/view-capsule.html?id=${data.capsule_id}`;
        currentCapsuleLink = capsuleLink;

        // Show success message
        const openDateFormatted = openDate.toLocaleDateString('tr-TR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
        document.getElementById('openDateDisplay').textContent = openDateFormatted;
        document.getElementById('viewCapsuleLink').href = capsuleLink;
        document.getElementById('successMessage').classList.remove('hidden');

        // Reset form
        document.getElementById('capsuleForm').reset();

        // Scroll to success message
        document.getElementById('successMessage').scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
        // Show error message
        document.getElementById('errorText').textContent = error.message;
        document.getElementById('errorMessage').classList.remove('hidden');

        // Scroll to error message
        document.getElementById('errorMessage').scrollIntoView({ behavior: 'smooth' });
    } finally {
        // Re-enable submit button
        submitBtn.disabled = false;
        submitBtn.textContent = 'Zaman Kapsülü Oluştur';
    }
});

// Copy capsule link to clipboard
function copyCapsuleLink() {
    if (!currentCapsuleLink) {
        alert('Henüz bir kapsül oluşturulmadı');
        return;
    }

    navigator.clipboard.writeText(currentCapsuleLink).then(() => {
        // Show success message
        document.getElementById('copyCapsuleSuccess').classList.remove('hidden');

        // Hide after 3 seconds
        setTimeout(() => {
            document.getElementById('copyCapsuleSuccess').classList.add('hidden');
        }, 3000);
    }).catch(err => {
        alert('Link kopyalanamadı: ' + err);
    });
}
