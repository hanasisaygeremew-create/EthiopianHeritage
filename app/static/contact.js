
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("contact-form");

    if (!form) return;

    form.addEventListener("submit", function (event) {
        const feedback = document.getElementById("contact-feedback");

        if (feedback) {
            feedback.textContent = "Sending your message...";
        }
    });
});
