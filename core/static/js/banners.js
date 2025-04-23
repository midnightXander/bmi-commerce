{/* <script> */}
// Banner management functions
function showBanner(type) {
    // Hide all banners first
    hideAllBanners();
    
    // Show the selected banner
    if (type === 'top') {
        document.getElementById('top-app-banner').classList.remove('hidden');
    } else if (type === 'bottom') {
        document.getElementById('bottom-app-banner').classList.remove('hidden');
    } else if (type === 'floating') {
        document.getElementById('floating-app-button').classList.remove('hidden');
    }
    
    // Store preference in localStorage to remember user's choice
    localStorage.setItem('appBannerPreference', type);
}

function hideAllBanners() {
    document.getElementById('top-app-banner').classList.add('hidden');
    document.getElementById('bottom-app-banner').classList.add('hidden');
    document.getElementById('floating-app-button').classList.add('hidden');
    document.getElementById('app-modal').classList.add('hidden');
}

// Event listeners for close buttons
// document.getElementById('close-top-banner').addEventListener('click', function() {
//     document.getElementById('top-app-banner').classList.add('hidden');
//     localStorage.setItem('topBannerDismissed', 'true');
// });

document.getElementById('close-bottom-banner').addEventListener('click', function() {
    console.log("clicked")
    document.getElementById('bottom-app-banner').classList.add('hidden');
    localStorage.setItem('bottomBannerDismissed', 'true');
});

// Floating button and modal functionality
// document.getElementById('open-app-modal').addEventListener('click', function() {
//     const modal = document.getElementById('app-modal');
//     modal.classList.toggle('hidden');
// });

// document.getElementById('close-app-modal').addEventListener('click', function() {
//     document.getElementById('app-modal').classList.add('hidden');
// });

// Close modal when clicking outside of it
document.addEventListener('click', function(event) {
    const modal = document.getElementById('app-modal');
    const button = document.getElementById('open-app-modal');
    
    if (!modal.classList.contains('hidden') && 
        !modal.contains(event.target) && 
        event.target !== button && 
        !button.contains(event.target)) {
        modal.classList.add('hidden');
    }
});

// Check for stored preference on page load
document.addEventListener('DOMContentLoaded', function() {
    const preference = localStorage.getItem('appBannerPreference');
    const topDismissed = localStorage.getItem('topBannerDismissed');
    const bottomDismissed = localStorage.getItem('bottomBannerDismissed');
    
    // if (preference && preference !== 'none') {
    //     if (preference === 'top' && topDismissed !== 'true') {
    //         showBanner('top');
    //     } else if (preference === 'bottom' && bottomDismissed !== 'true') {
    //         showBanner('bottom');
    //     } else if (preference === 'floating') {
    //         showBanner('floating');
    //     }
    // } else {
    //     // Default banner if no preference is set
    //     showBanner('top');
    // }
});
// </script>