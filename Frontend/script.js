document.addEventListener("DOMContentLoaded", function () {
    // Adding event listeners to feature boxes
    document.querySelectorAll(".feature-box").forEach(box => {
        box.addEventListener("click", async function () {
            const feature = this.getAttribute("data-feature");
            const promptNumber = getFeatureNumber(feature);
            showLoadingPopup(); // Show loading while fetching data
            const responseText = await fetchAIResponse(promptNumber);
            hideLoadingPopup(); // Hide loading spinner
            showPopup(responseText);
        });
    });

    // Mapping features to their respective prompt numbers
    function getFeatureNumber(feature) {
        const promptNumbers = {
            "data-analysis": 1,
            "budgeting": 2,
            "expense-management": 3,
            "investment": 4,
            "chatbot": 5
        };
        return promptNumbers[feature] || 0;
    }

    // Fetching the AI response from the API
    async function fetchAIResponse(promptNumber) {
        try {
            const response = await fetch("http://127.0.0.1:5000/api/process-prompt", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ prompt_number: promptNumber })
            });
            const data = await response.json();
            return data.response || "No response received.";  // Handle empty response
        } catch (error) {
            console.error("Error fetching AI response:", error);
            return "Error processing request."; // Show error message on failure
        }
    }

    // Displaying a popup with the AI response text
    function showPopup(text) {
        // Remove any existing popups before creating a new one
        document.querySelectorAll(".popup").forEach(popup => popup.remove());

        const popup = document.createElement("div");
        popup.classList.add("popup");
        popup.innerHTML = `
            <div class="popup-content">
                <p>${text}</p>
                <button onclick="this.closest('.popup').remove()">Close</button>
            </div>
        `;
        document.body.appendChild(popup);
    }

    // Show loading popup
    function showLoadingPopup() {
        const loadingPopup = document.createElement("div");
        loadingPopup.classList.add("popup", "loading");
        loadingPopup.innerHTML = `
            <div class="popup-content">
                <p>Loading...</p>
            </div>
        `;
        document.body.appendChild(loadingPopup);
    }

    // Hide loading popup
    function hideLoadingPopup() {
        const loadingPopups = document.querySelectorAll(".popup.loading");
        loadingPopups.forEach(popup => popup.remove());
    }
});

async function fetchStockCSV() {
    try {
        const response = await fetch("./assets/stock_data.csv");
        const csvText = await response.text();
        const parsedData = Papa.parse(csvText, { header: true }).data;

        function parseDate(dateStr) {
            const months = { Jan: 0, Feb: 1, Mar: 2, Apr: 3, May: 4, Jun: 5, Jul: 6, Aug: 7, Sep: 8, Oct: 9, Nov: 10, Dec: 11 };
            const parts = dateStr.split("-");
            if (parts.length !== 3) return null;

            const day = parseInt(parts[0], 10);
            const month = months[parts[1]];
            const year = parseInt(parts[2], 10) + 2000;

            return new Date(year, month, day);
        }

        const cleanedData = parsedData
            .filter(entry => entry.Date && entry.Close && entry.Volume)
            .map(entry => ({
                date: parseDate(entry.Date),
                close: parseFloat(entry.Close.replace(/,/g, "")) || 0,
                volume: parseInt(entry.Volume.replace(/,/g, ""), 10) || 0
            }))
            .filter(entry => entry.date);

        cleanedData.sort((a, b) => a.date - b.date);

        const sortedLabels = cleanedData.map(entry => entry.date);
        const sortedClosingPrices = cleanedData.map(entry => entry.close);
        const sortedVolumes = cleanedData.map(entry => entry.volume);

        const ctx = document.getElementById("metricsChart").getContext("2d");
        new Chart(ctx, {
            type: "bar",
            data: {
                labels: sortedLabels,
                datasets: [
                    {
                        type: "line",
                        label: "Price (INR)",
                        data: sortedClosingPrices,
                        borderColor: "#00FF00", // Bright Green Line
                        borderWidth: 2, // You can increase borderWidth for a thicker line
                        pointRadius: 0,
                        fill: false, // Set to false to keep it a line without filling
                        yAxisID: "y",
                    },
                    
                    {
                        type: "bar",
                        label: "Volume",
                        data: sortedVolumes,
                        backgroundColor: "rgba(0, 123, 255, 0.1)",
                        borderColor: "rgba(25, 136, 255, 0.3)",
                        borderWidth: 1,
                        yAxisID: "y1",
                        barPercentage: 0.8,
                        categoryPercentage: 0.9
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                interaction: { mode: "index", intersect: false },
                plugins: {
                    tooltip: {
                        enabled: true,
                        callbacks: {
                            title: tooltipItems => new Date(tooltipItems[0].label).toDateString(),
                            label: tooltipItem => 
                                tooltipItem.datasetIndex === 0 
                                ? `Close: ₹ ${tooltipItem.raw.toFixed(2)}` 
                                : `Volume: ${tooltipItem.raw.toLocaleString()}`
                        }
                    },
                    legend: {
                        labels: {
                            color: "white" // Make legend text white
                        }
                    }
                },
                scales: {
                    x: {
                        type: "time",
                        time: { unit: "day", tooltipFormat: "MMM d, yyyy", displayFormats: { day: "MMM d" } },
                        title: { display: true, text: "Date", color: "white" }, // Make title white
                        ticks: { color: "white", autoSkip: true, maxTicksLimit: 10 } // Make axis labels white
                    },
                    y: { 
                        title: { display: true, text: "Closing Price (INR)", color: "white" }, 
                        ticks: { color: "white" }, // Make axis labels white
                        beginAtZero: false 
                    },
                    y1: { 
                        position: "right", 
                        title: { display: true, text: "Volume", color: "white" }, 
                        ticks: { color: "white" }, // Make axis labels white
                        beginAtZero: true, 
                        grid: { drawOnChartArea: false } 
                    }
                }
            }                        
        });

    } catch (error) {
        console.error("Error fetching stock data:", error);
    }
}

async function fetchCompanyCSV() {
    try {
        const response = await fetch("./assets/Company.csv");
        const csvText = await response.text();
        const parsedData = Papa.parse(csvText, { header: true }).data[0]; // Single-company data

        const getValue = (key, isCurrency = false, isPercentage = false) => {
            let value = parsedData[key] || "N/A";
            
            value = value.toString().replace(/[^\d.]/g, ""); 
            
            if (!isNaN(value) && value !== "") {
                value = parseFloat(value);
                if (isPercentage) value = Math.min(value, 100);
            } else {
                value = "N/A";
            }
            
            return isCurrency && value !== "N/A" ? `${value.toLocaleString()}` : value;
        };

        document.getElementById("currentPrice").textContent = getValue("CurentPrice", true);
        document.getElementById("high").textContent = getValue("High", true);
        document.getElementById("low").textContent = getValue("Low", true);
        document.getElementById("marketCap").textContent = getValue("MCap", true);
        document.getElementById("stockPE").textContent = parsedData["StockPE"] || "N/A";
        document.getElementById("pat").textContent = getValue("PAT", true);
        document.getElementById("reserves").textContent = getValue("Reserves", true);
        document.getElementById("debtToEquity").textContent = getValue("DebttoEquity");
        document.getElementById("evebitda").textContent = getValue("EVEBITDA");

        function createDoughnutChart(canvasId, value, label) {
            const ctx = document.getElementById(canvasId).getContext("2d");
        
            new Chart(ctx, {
                type: "doughnut",
                data: {
                    labels: [label, "Remaining"],
                    datasets: [{
                        data: [value, 100 - value],
                        backgroundColor: ["#007bff", "#e9ecef"],
                        borderColor: ["#ffffff", "#ffffff"],
                        borderWidth: 2,
                        hoverOffset: 8
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: "70%", // Larger cutout for a cleaner look
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: (tooltipItem) => `${tooltipItem.raw.toFixed(2)}%`
                            }
                        }
                    }
                },
                plugins: [{
                    id: "centerText",
                    beforeDraw(chart) {
                        const { width } = chart;
                        const { ctx } = chart;
                        const { datasets } = chart.data;
        
                        ctx.save();
        
                        const centerX = width / 2;
                        const centerY = chart.chartArea.top + (chart.chartArea.bottom - chart.chartArea.top) / 2;
        
                        const mainValue = datasets[0].data[0] || 0;
        
                        ctx.font = "bold 16px Arial";
                        ctx.fillStyle = "white"; // Set the text color to white
                        ctx.textAlign = "center";
                        ctx.textBaseline = "middle";
        
                        ctx.fillText(`${mainValue.toFixed(1)}%`, centerX, centerY);
        
                        ctx.restore();
                    }
                }]
            });
        }        

        createDoughnutChart("salesVarChart", 34.98, "Sales Var");
        createDoughnutChart("return5yrsChart", 43.99, "5Y Return");
        createDoughnutChart("cagrChart", 44, "CAGR");
        createDoughnutChart("roeChart", 15, "ROE");
        createDoughnutChart("profitVarChart", 36, "Profit Var");

    } catch (error) {
        console.error("Error loading company data:", error);
    }
}

window.onload = function() {
    fetchStockCSV();
    fetchCompanyCSV();
};