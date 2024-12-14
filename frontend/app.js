document.getElementById("api-call").addEventListener("click", async () => {
    try {
        const response = await fetch('/api/health-check');
        const data = await response.json();
        document.getElementById("api-response").textContent = `Status: ${data.status}, Message: ${data.message}`;
    } catch (error) {
        document.getElementById("api-response").textContent = "Error: Unable to connect to the backend.";
    }
});
