var ctx=document.getElementById("myAreaChart");
var myLineChart = new Chart(ctx,{type:"line",
    data:{
        labels:["Mar 1","Mar 2","Mar 3","Mar 4","Mar 5","Mar 6","Mar 7","Mar 8","Mar 9","Mar 10","Mar 11","Mar 12","Mar 13"],
        datasets:[
            {
                label:"Sessions",
                lineTension:.3,
                backgroundColor:"rgba(2,117,216,0.2)",
                borderColor:"rgba(2,117,216,1)",
                pointRadius:5,
                pointBackgroundColor:"rgba(2,117,216,1)",
                pointBorderColor:"rgba(255,255,255,0.8)",
                pointHoverRadius:5,
                pointHoverBackgroundColor:"rgba(2,117,216,1)",
                pointHitRadius:20,
                pointBorderWidth:2,
                data:[1,3,5,7,9,11,2,4,6,8,10,12]
            }
        ]
    },
    options:{scales:{xAxes:[{time:{unit:"date"},
    gridLines:{display:!1},
    ticks:{maxTicksLimit:7}}],
    yAxes:[{ticks:{min:0,max:20,maxTicksLimit:5},
    gridLines:{color:"rgba(0, 0, 0, .125)"}}]},
    legend:{display:!1}}});