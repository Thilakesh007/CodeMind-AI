function startSession(){
  const name = document.getElementById("student").value;
  if(!name){
    alert("Enter student name");
    return;
  }
  fetch("/start?student="+encodeURIComponent(name));
}

function stopSession(){
  const student = document.getElementById("student").value;
  if(!student){
    alert("Enter student name");
    return;
  }

  fetch("/stop?student="+encodeURIComponent(student))
    .then(() => stopCamera());   // 🔥 CAMERA OFF
}

setInterval(() => {
  const student = document.getElementById("student").value;
  if (!student) return;

  fetch('/data?student=' + encodeURIComponent(student))
    .then(r => r.json())
    .then(d => {
      if (!d.presence && d.presence !== 0) return;

      document.getElementById("p").innerText = d.presence;
      document.getElementById("et").innerText = d.engagement_time;
      document.getElementById("e").innerText = d.engagement;
      document.getElementById("a").innerText = d.attention;
      document.getElementById("mv").innerText = d.movement;
      document.getElementById("at").innerText = d.attendance;
      document.getElementById("el").innerText = d.engagement_level;
      document.getElementById("studentNameDisplay").innerText = d.student_name;
      document.getElementById("sname").innerText = d.student_name;

      const badge = document.getElementById("statusBadge");
      badge.className =
        d.movement.includes("Engaged") ? "badge engaged" :
        d.movement.includes("Distracted") ? "badge distracted" :
        "badge neutral";

      badge.innerText = d.movement;

      // 🔥 GRAPH UPDATE
      updateChart(d.engagement, d.attention);

    });
}, 1000);
