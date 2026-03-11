// Test script to verify handshake functionality
const testHandshake = async () => {
    const categories = ["Science", "Health", "Industry", "Develop"];

    console.log("Testing CIGOL Handshake System\n" + "=".repeat(50));

    for (const category of categories) {
        try {
            const response = await fetch("http://127.0.0.1:8000/handshake", {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    active_module: category,
                    sync_ratio: 1.618
                })
            });

            const data = await response.json();
            console.log(`✓ ${category}: ${data.status} - Focus: ${data.focus}`);
        } catch (error) {
            console.log(`✗ ${category}: Failed - ${error.message}`);
        }
    }

    console.log("=".repeat(50));
    console.log("Test complete! Check backend terminal for 'SYSTEM DEDICATED TO' messages.");
};

testHandshake();
