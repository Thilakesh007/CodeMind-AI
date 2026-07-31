function sendMetrics(face, ear, mar, headTurn) {
  const student = document.getElementById("student").value;
  if (!student) return;

  fetch("/metrics", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      student: student,
      face: face,
      ear: ear,
      mar: mar,
      head: headTurn
    })
  });
}
