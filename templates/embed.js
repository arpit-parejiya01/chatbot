document.addEventListener("DOMContentLoaded", function () {
    const iframe = document.createElement("iframe");
    iframe.id = "chatbot-iframe";
    iframe.style.width = "400px";
    iframe.style.height = "600px";
    iframe.style.border = "none";
    iframe.style.position = "fixed";
    iframe.style.bottom = "20px";
    iframe.style.right = "20px";
    iframe.style.boxShadow = "0 4px 8px rgba(0, 0, 0, 0.2)";
    iframe.src = "http://192.168.2.77:5000"; // Use the full URL to your Flask app
    document.body.appendChild(iframe);
});
