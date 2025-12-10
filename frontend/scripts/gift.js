// Global variable to store gift link
let currentGiftLink = '';

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Gift form handler
    const giftForm = document.getElementById('giftForm');
    if (!giftForm) {
        console.error('Gift form not found');
        return;
    }

    giftForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Get form elements
        const senderNameEl = document.getElementById('sender_name');
        const recipientNameEl = document.getElementById('recipient_name');
        const recipientEmailEl = document.getElementById('recipient_email');
        const cardTemplateEl = document.querySelector('input[name="card_template"]:checked');
        const messageEl = document.getElementById('message');

        // Validate all required elements exist
        if (!senderNameEl || !recipientNameEl || !recipientEmailEl || !cardTemplateEl || !messageEl) {
            const errorText = document.getElementById('errorText');
            if (errorText) {
                errorText.textContent = 'Form alanları bulunamadı. Lütfen sayfayı yenileyin.';
                const errorMessage = document.getElementById('errorMessage');
                if (errorMessage) {
                    errorMessage.classList.remove('hidden');
                }
            }
            return;
        }

        // Get form data
        const formData = {
            sender_name: senderNameEl.value,
            recipient_name: recipientNameEl.value,
            recipient_email: recipientEmailEl.value,
            card_template: cardTemplateEl.value,
            message: messageEl.value
        };

        // Disable submit button
        const submitBtn = document.getElementById('submitBtn');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.textContent = 'Gönderiliyor...';
        }

        // Hide previous messages
        const successMessage = document.getElementById('successMessage');
        const errorMessage = document.getElementById('errorMessage');
        const copySuccess = document.getElementById('copySuccess');
        
        if (successMessage) successMessage.classList.add('hidden');
        if (errorMessage) errorMessage.classList.add('hidden');
        if (copySuccess) copySuccess.classList.add('hidden');

        try {
            const response = await fetch('http://localhost:5000/api/gifts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Hediye gönderilemedi');
            }

            // Store gift link globally
            currentGiftLink = data.view_link;

            // Show success message
            const viewLink = document.getElementById('viewLink');
            if (viewLink) {
                viewLink.href = data.view_link;
            }
            if (successMessage) {
                successMessage.classList.remove('hidden');
            }

            // Reset form
            if (giftForm) {
                giftForm.reset();
            }

            // Scroll to success message
            if (successMessage) {
                successMessage.scrollIntoView({ behavior: 'smooth' });
            }

        } catch (error) {
            // Show error message
            const errorText = document.getElementById('errorText');
            if (errorText) {
                errorText.textContent = error.message;
            }
            if (errorMessage) {
                errorMessage.classList.remove('hidden');
                errorMessage.scrollIntoView({ behavior: 'smooth' });
            }
        } finally {
            // Re-enable submit button
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Hediye Gönder';
            }
        }
    });
});

// Copy gift link to clipboard
function copyGiftLink() {
    if (!currentGiftLink) {
        alert('Henüz bir hediye oluşturulmadı');
        return;
    }

    navigator.clipboard.writeText(currentGiftLink).then(() => {
        // Show success message
        const copySuccess = document.getElementById('copySuccess');
        if (copySuccess) {
            copySuccess.classList.remove('hidden');
            // Hide after 3 seconds
            setTimeout(() => {
                copySuccess.classList.add('hidden');
            }, 3000);
        }
    }).catch(err => {
        alert('Link kopyalanamadı: ' + err);
    });
}
