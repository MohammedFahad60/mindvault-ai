/**
 * MindVault Pro: Frontend Controller
 * Implements: Markdown Rendering, Auto-Scroll, & State Management
 */

// 1. Markdown Configuration (Professional Formatting)
marked.setOptions({
    breaks: true,   // Converts single line breaks to <br>
    gfm: true,      // GitHub Flavored Markdown
    sanitize: false // Allows the HTML we specifically define
});

async function sendMessage() {
    const input = document.getElementById('user-input');
    const msg = input.value.trim();
    
    // Validate Input
    if (!msg) return;

    // A. Add User Bubble immediately for better UX
    appendMessage('user', msg);
    input.value = '';

    // B. Show Professional "Analyzing" State
    const typingIndicator = appendMessage('bot', `
        <div class="d-flex align-items-center gap-2">
            <div class="spinner-grow spinner-grow-sm text-info" role="status"></div>
            <span>Securing your data & analyzing...</span>
        </div>
    `);

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ message: msg })
        });

        if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);

        const data = await response.json();
        
        // Remove typing indicator with a slight delay for smooth feel
        typingIndicator.remove();

        // C. Render Advanced Markdown Response
        // This converts **bold** to <b> and \n to paragraphs
        const formattedReply = marked.parse(data.reply);
        appendMessage('bot', formattedReply);

    } catch (error) {
        console.error("Critical Connection Error:", error);
        typingIndicator.innerHTML = `
            <div class="alert alert-danger m-0 py-1">
                <i class="fas fa-exclamation-triangle"></i> 
                Vault Connection Offline. Data remains encrypted locally.
            </div>`;
    }
}

/**
 * Professional DOM Injector
 * Handles bubble creation, styling, and scroll-to-view
 */
function appendMessage(sender, htmlContent) {
    const chatWindow = document.getElementById('chat-window');
    
    // Create the message container
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender} animate-in`;
    
    // Add Role Label for Professional Look
    const label = sender === 'bot' 
        ? `<div class="mb-1"><small class="text-info"><i class="fas fa-robot"></i> AI Companion</small></div>`
        : `<div class="mb-1 text-end"><small class="text-white-50">You</small></div>`;
    
    messageDiv.innerHTML = label + htmlContent;
    
    chatWindow.appendChild(messageDiv);

    // D. Smooth Auto-Scroll to latest message
    messageDiv.scrollIntoView({ behavior: 'smooth', block: 'end' });
    
    return messageDiv;
}

// Support for "Enter" key submission
document.getElementById('user-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});