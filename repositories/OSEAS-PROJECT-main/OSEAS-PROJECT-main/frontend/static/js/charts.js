const ctx=document.getElementById("chart");
const chart=new Chart(ctx,{
type:"line",
data:{
labels:[],
datasets:[
{label:"Engagement %",data:[],borderColor:"#22c55e",borderWidth:2},
{label:"Attention %",data:[],borderColor:"#3b82f6",borderWidth:2}
]},
options:{scales:{y:{min:0,max:100}}}
});

function updateChart(engagement, attention){
  const timeLabel = new Date().toLocaleTimeString();

  // limit graph points to last 20
  if (chart.data.labels.length > 20) {
    chart.data.labels.shift();
    chart.data.datasets[0].data.shift();
    chart.data.datasets[1].data.shift();
  }
  chart.data.labels.push(timeLabel);
  chart.data.datasets[0].data.push(engagement);
  chart.data.datasets[1].data.push(attention);
  chart.update();
}
