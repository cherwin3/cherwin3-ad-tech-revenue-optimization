    const axios = require("axios");

const FASTAPI_URL =
    process.env.FASTAPI_URL || "http://localhost:8000";

async function requestOptimization(adRequest) {
    const response = await axios.post(
        `${FASTAPI_URL}/optimize-placement`,
        adRequest,
        {
            timeout: 10000,
            headers: {
                "Content-Type": "application/json"
            }
        }
    );

    return response.data;
}

module.exports = {
    requestOptimization
};