document.addEventListener("DOMContentLoaded", () => {
    const guessInput = document.querySelector('input[name="guess"]');
    if (!guessInput) {
        return;
    }

    guessInput.addEventListener("input", () => {
        guessInput.value = guessInput.value.replace(/[^a-z]/gi, "").toUpperCase().slice(0, 5);
    });
});
