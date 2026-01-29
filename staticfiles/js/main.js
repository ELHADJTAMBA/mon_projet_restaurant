document.addEventListener('DOMContentLoaded', function() {
    
    // Auto-dismiss des messages après 5 secondes
    const messages = document.querySelectorAll('.message-alert');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.transition = 'opacity 0.5s';
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 500);
        }, 5000);
    });
    
    // Confirmation avant suppression
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm(this.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });
    
    // Mise à jour en temps réel du total du panier
    const quantityInputs = document.querySelectorAll('input[name="quantite"]');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const min = parseInt(this.min);
            const max = parseInt(this.max);
            let value = parseInt(this.value);
            
            if (value < min) this.value = min;
            if (value > max) this.value = max;
        });
    });
    
    // Recherche de plats (si formulaire de recherche existe)
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        const searchInput = document.getElementById('search-input');
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                searchForm.submit();
            }, 500);
        });
    }
    
    // Actualisation automatique pour les serveurs (toutes les 30 secondes)
    if (document.body.dataset.role === 'Rservent' || document.body.dataset.role === 'Radmin') {
        setInterval(() => {
            // Vérifier s'il y a de nouvelles commandes
            // Cette fonctionnalité peut être implémentée avec AJAX
            console.log('Vérification des nouvelles commandes...');
        }, 30000);
    }
    
});

// Fonction pour formater les prix
function formatPrice(price) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'GNF',
        minimumFractionDigits: 0
    }).format(price);
}

// Fonction pour imprimer
function printPage() {
    window.print();
}

// Fonction pour exporter en PDF (nécessite une bibliothèque côté serveur)
function exportToPDF() {
    window.location.href = window.location.pathname + '?export=pdf';
}

// Notification sonore (optionnel)
function playNotification() {
    // Ajouter un son de notification si nécessaire
    const audio = new Audio('/static/sounds/notification.mp3');
    audio.play().catch(e => console.log('Notification sound failed', e));
}