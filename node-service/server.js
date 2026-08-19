require("dotenv").config();

const express = require("express");
const { requestOptimization } = require("./fastapiClient");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get("/", (request, response) => {
    response.json({
        message: "Node.js Ad Placement Service is running"
    });
});

app.get("/health", (request, response) => {
    response.json({
        node_service: "healthy"
    });
});

app.post("/ad-placement", async (request, response) => {
    try {
        const result = await requestOptimization(request.body);

        response.status(200).json({
            status: "success",
            optimization: result
        });
    } catch (error) {
        const statusCode = error.response?.status || 503;

        response.status(statusCode).json({
            status: "error",
            message: "Unable to process ad placement",
            details:
                error.response?.data ||
                error.message
        });
    }
});

app.listen(PORT, () => {
    console.log(
        `Node.js service running at http://localhost:${PORT}`
    );
});