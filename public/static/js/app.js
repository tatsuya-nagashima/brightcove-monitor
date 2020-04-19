const server = "localhost:5000";

window.onload = () => {
  update_state();
  update_viewers();

  setInterval(update_time, 1000);
  setInterval(update_state, 60000);
  setInterval(update_viewers, 60000);
};

function update_time() {
  const d = new Date();
  const year = d.getFullYear();
  const month = d.getMonth() + 1;
  const day = d.getDate();
  const hour = d.getHours() < 10 ? "0" + d.getHours() : d.getHours();
  const min = d.getMinutes() < 10 ? "0" + d.getMinutes() : d.getMinutes();
  const sec = d.getSeconds() < 10 ? "0" + d.getSeconds() : d.getSeconds();

  document.getElementById("date").innerHTML = year + "/" + month + "/" + day + " " + hour + ":" + min + ":" + sec;
}

function update_state() {
  const url = "http://" + server + "/state";
  const xhr = new XMLHttpRequest();
  xhr.open("GET", url);
  xhr.send();
  xhr.onreadystatechange = () => {
    if (xhr.readyState === 4 && xhr.status === 200) {
      const res = JSON.parse(xhr.responseText);
      document.getElementById("state").innerHTML = res["state"];
    }
  };
}

function update_viewers() {
  const url = "http://" + server + "/viewers";
  const xhr = new XMLHttpRequest();
  xhr.open("GET", url);
  xhr.send();
  xhr.onreadystatechange = () => {
    if (xhr.readyState === 4 && xhr.status === 200) {
      const res = JSON.parse(xhr.responseText);

      let tbody = document.getElementById("tbody");
      while (tbody.rows.length > 0) tbody.deleteRow(-1);
      for (let i = 0; i < res["timestamp"].length; i++) {
        let tr = document.createElement("tr");
        let td1 = document.createElement("td");
        let td2 = document.createElement("td");

        tbody.appendChild(tr);
        tr.appendChild(td1);
        tr.appendChild(td2);
        td1.innerHTML = res["timestamp"][i];
        td2.innerHTML = res["viewers"][i];
      }
    }
  };
}

function download_log() {
  document.body.style.cursor = "wait";
  const date = document.getElementById("datepicker").value;
  const url = "http://" + server + "/log/" + date;
  const xhr = new XMLHttpRequest();
  xhr.open("GET", url);
  xhr.send();
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      const res = JSON.parse(xhr.responseText);
      const blob = new Blob([res["log"]], { type: "text/plain" });
      let link = document.createElement("a");
      link.href = window.URL.createObjectURL(blob);
      link.download = date + ".csv";
      link.click();

      document.body.style.cursor = "auto";
    }
  };
}
