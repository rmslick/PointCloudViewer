function showNotification(message, type = 'info') {
    const notificationContainer = document.getElementById('notification-container');
  
    // Create the notification element
    const notification = document.createElement('div');
    notification.classList.add('alert', `alert-${type}`, 'alert-dismissible', 'fade', 'show');
    notification.setAttribute('role', 'alert');
  
    // Add the message to the notification
    notification.innerText = message;
  
    // Add the close button to the notification
    const closeButton = document.createElement('button');
    closeButton.classList.add('btn-close');
    closeButton.setAttribute('type', 'button');
    closeButton.setAttribute('data-bs-dismiss', 'alert');
    closeButton.setAttribute('aria-label', 'Close');
    notification.appendChild(closeButton);
  
    // Add the notification to the container
    notificationContainer.appendChild(notification);
  }
  