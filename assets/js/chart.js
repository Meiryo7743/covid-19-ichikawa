// Modify Chart.js Global Settings
const configureChart = () => {
  Chart.defaults.global.defaultFontColor = "#84919e";
  Chart.defaults.global.defaultFontFamily = "'Roboto','Helvetica',sans-serif";
  Chart.defaults.global.devicePixelRatio = 3;
  Chart.defaults.global.responsive = false;
};

configureChart();

// Draw a Chart
const drawChart = function (ID, DATA) {
  const data = JSON.parse(JSON.stringify(DATA));
  const ctx = document.getElementById(ID).getContext("2d");
  const renderChart = new Chart(ctx, data);
};
