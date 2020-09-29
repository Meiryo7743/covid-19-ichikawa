function sortTable(TABLE, TBODY) {
  const tbody = document.getElementById(TBODY);
  tbody.className = "list";
  const options = {
    valueNames: ["市内", "県内", "検査確定日", "発症日"],
  };
  const userList = new List(TABLE, options);
}
