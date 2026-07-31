function filterTable(){
  let input=document.getElementById("search").value.toUpperCase();
  let rows=document.querySelectorAll("table tr");
  rows.forEach((r,i)=>{
    if(i===0) return;
    r.style.display = r.innerText.toUpperCase().includes(input) ? "" : "none";
  });
}
