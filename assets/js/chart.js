// Chart.js global settings
Chart.defaults.global.defaultFontColor = "#84919e";
Chart.defaults.global.defaultFontFamily = "'Roboto','Helvetica',sans-serif";
Chart.defaults.global.devicePixelRatio = 3;
Chart.defaults.global.responsive = false;

// Draw chart
function drawChart(ID, DATA) {
  // Chart block-size
  document.getElementById(ID).style.blockSize = "20rem";

  const data = JSON.parse(JSON.stringify(DATA));
  const ctx = document.getElementById(ID).getContext("2d");
  const renderChart = new Chart(ctx, data);
}
