const drawColumnChart = (id, source) => {
  google.charts.load("current", { packages: ["corechart"] });
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    const obj = JSON.parse(JSON.stringify(source));

    const data = new google.visualization.DataTable();
    for (let i = 0; i < obj.data.headers.length; i++) {
      data.addColumn(obj.data.headers[i]["type"], obj.data.headers[i]["name"]);
    }
    data.addRows(obj.data.rows);

    new google.visualization.ColumnChart(document.getElementById(id)).draw(
      data,
      obj.options
    );

    // Callback
    setTimeout(function () {
      moveToEnd(id);
    });
  }
};

// Set the initial position of the horizontal scroll to the end.
const moveToEnd = (id) => {
  const target = document.getElementById(id);
  const width = document.querySelector(`#${id} svg`).clientWidth;
  target.parentElement.scrollLeft += width;
};
