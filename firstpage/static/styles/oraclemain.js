//import Datafeed from './datafeed.js';

//import { createChart } from 'lightweight-charts';


//  <script src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>

$(document).ready(function(){
    $("#chartsearchbutton").click(function(){
      var firstsymbol = $("#firstchart").val();
      var secondsymbol = $("#secondchart").val();
      console.log(" ================ ");
      console.log(firstsymbol, '    ', secondsymbol);
      console.log(" ================ ");
      var temp = new TradingView.widget(
            {
            "autosize": true,
            "symbol": firstsymbol,
            "interval": "D",
            "timezone": "Etc/UTC",
            "theme": "light",
            "style": "1",
            "locale": "en",
            "toolbar_bg": "#f1f3f6",
            "enable_publishing": false,
            "allow_symbol_change": false,
            "container_id": "tradingview_f6874"
          }
      );
      var temp2 = new TradingView.widget(
            {
            "autosize": true,
            "symbol": secondsymbol,
            "interval": "D",
            "timezone": "Etc/UTC",
            "theme": "light",
            "style": "1",
            "locale": "en",
            "toolbar_bg": "#f1f3f6",
            "enable_publishing": false,
            "allow_symbol_change": false,
            "container_id": "tradingview_f6875"
          }
      );


      const chartProperties = {
          width:1000,
          height:250,
          timeScale:{
          timeVisible:true,
          secondsVisible:false,
          }
      }
    
      /*
      const domElement = document.getElementById('tradingview_f6876');
      console.log(" ================ ");
      console.log(domElement);
      console.log(" ================ ");
      const chart = createChart(domElement,chartProperties);
      chart.resize(500,600)
      console.log(" chart created " );
      const candleSeries = chart.addCandlestickSeries();
      console.log(" candleSeries added ");
      */

      const postdata = {};
      postdata["stock"] = firstsymbol;
      postdata['period'] = 'max';
      postdata['interval'] = '1d';
      console.log(" post data   ", postdata);
      axios({
        method: 'post',
//        url: 'http://127.0.0.1:8000/historical',
        url: '/historical',
        data: postdata,
        headers: {"Content-Type": "application/json"}
      }).then((data) => {

        console.log(" first rawdata   ", data.data);
        var firstdata = [];
        var firstdataopen = [];
        var firstdatahigh = [];
        var firstdatalow = [];
        var firstdataclose = [];
        for (var i = data.data.date.length-1; i >= 0; i--){
            firstdata.push(data.data.date[i]);
            firstdataopen.push(data.data.open[i]);
            firstdatahigh.push(data.data.high[i]);
            firstdatalow.push(data.data.low[i]);
            firstdataclose.push(data.data.close[i]);
            
            if (firstdata.length >= 3650){
                break;
            }
            
        }
        firstdata.reverse();
        firstdataopen.reverse();
        firstdatahigh.reverse();
        firstdatalow.reverse();
        firstdataclose.reverse();

        console.log(" first data  ", firstdata);
    
    
        const postdata2 = {};
        postdata2["stock"] = secondsymbol;
        postdata2['period'] = 'max';
        postdata2['interval'] = '1d';

        console.log(" second post data    ", postdata2);
    
        axios({
            method: 'post',
//            url: 'http://127.0.0.1:8000/historical',
            url: '/historical',
            data: postdata2,
            headers: {"Content-Type": "application/json"}
          }).then((data2) => {

            console.log(" second rawdata   ", data2.data);
    
            var seconddata = [];
            var seconddataopen = [];
            var seconddatahigh = [];
            var seconddatalow = [];
            var seconddataclose = [];
            for (var i = data2.data.date.length-1; i >= 0; i--){
                seconddata.push(data2.data.date[i]);
                seconddataopen.push(data2.data.open[i]);
                seconddatahigh.push(data2.data.high[i]);
                seconddatalow.push(data2.data.low[i]);
                seconddataclose.push(data2.data.close[i]);
                if (seconddata.length >= 3650){
                  break;
                }
            }
            seconddata.reverse();
            seconddataopen.reverse();
            seconddatahigh.reverse();
            seconddatalow.reverse();
            seconddataclose.reverse();

            console.log(" second data   ", seconddata);
    
            var spreaddate = [];
            var spreadopen = [];
            var spreadhigh = [];
            var spreadlow = [];
            var spreadclose = [];
            for (var i = 0; i < firstdata.length; i ++){
              var currdate = firstdata[i];
              for (var j = 0; j < seconddata.length; j++){
                if (currdate == seconddata[j]){
                  spreaddate.push(currdate);
                  spreadopen.push(firstdataopen[i]/seconddataopen[j]);
                  spreadhigh.push(firstdatahigh[i]/seconddatahigh[j]);
                  spreadlow.push(firstdatalow[i]/seconddatalow[j]);
                  spreadclose.push(firstdataclose[i]/seconddataclose[j]);
                }
              }
    
            };

          

            var chartdata = [];
            for (var i = 0; i < spreaddate.length; i++){
              chartdata.push([spreaddate[i]*1000, spreadclose[i]]);
              // spreadopen[i], spreadhigh[i], spreadlow[i], 
            }

            console.log("chart data   ", chartdata);

            var chartdata2 = [];
            for (var i = chartdata.length-1; i >= 0; i--){
                chartdata2.push(chartdata[i]);
                if (chartdata2.length >= 365){
                  break;
                }
            }
            chartdata2.reverse();


            /*
            Highcharts.stockChart('tradingview_f6876', {
                navigation: {
                    bindings: {
                        rect: {
                            annotationsOptions: {
                                shapeOptions: {
                                    fill: 'rgba(255, 0, 0, 0.8)'
                                }
                            }
                        }
                    },
                    annotationsOptions: {
                        typeOptions: {
                            line: {
                                stroke: 'rgba(255, 0, 0, 1)',
                                strokeWidth: 10
                            }
                        }
                    }
                },
                yAxis: [{
                    labels: {
                        align: 'left'
                    },
                    height: '80%'
                }, {
                    labels: {
                        align: 'left'
                    },
                    top: '80%',
                    height: '20%',
                    offset: 0
                }],
                series: [{
                    type: 'ohlc',
                    id: 'spread-ohlc',
                    name: 'Stock Spread',
                    data: chartdata
                }
                /* {
                    type: 'column',
                    id: 'aapl-volume',
                    name: 'AAPL Volume',
                    data: volume,
                    yAxis: 1
                }
                */
                /*
                ]
            });
            */
      
            var spreadname = firstsymbol.toUpperCase() + " / " + secondsymbol.toUpperCase() + " Spread";
        
            Highcharts.stockChart('tradingview_f6876', {
              navigation: {
                  bindings: {
                      rect: {
                          annotationsOptions: {
                              shapeOptions: {
                                  fill: 'rgba(255, 0, 0, 0.8)'
                              }
                          }
                      }
                  },
                  annotationsOptions: {
                      typeOptions: {
                          line: {
                              stroke: 'rgba(255, 0, 0, 1)',
                              strokeWidth: 10
                          }
                      }
                  }
              },
              yAxis: [{
                  labels: {
                      align: 'left'
                  },
                  height: '80%'
              }, {
                  labels: {
                      align: 'left'
                  },
                  top: '80%',
                  height: '20%',
                  offset: 0
              }],
              series: [{
                  type: 'line',
                  id: 'spread-ohlc',
                  name: spreadname,
                  data: chartdata2
              }
              /* {
                  type: 'column',
                  id: 'aapl-volume',
                  name: 'AAPL Volume',
                  data: volume,
                  yAxis: 1
              }
              */
              
              ]
          });
            






            /*
            Highcharts.chart('tradingview_f6876', {
                chart: {
                    zoomType: 'x'
                },
                xAxis: {
                    type: 'datetime'
                },
                yAxis: {
                    title: {
                        text: 'Spread'
                    }
                },
                legend: {
                    enabled: false
                },
                plotOptions: {
                    area: {
                        fillColor: {
                            linearGradient: {
                                x1: 0,
                                y1: 0,
                                x2: 0,
                                y2: 1
                            },
                            stops: [
                                [0, Highcharts.getOptions().colors[0]],
                                [1, Highcharts.color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                            ]
                        },
                        marker: {
                            radius: 2
                        },
                        lineWidth: 1,
                        states: {
                            hover: {
                                lineWidth: 1
                            }
                        },
                        threshold: null
                    }
                },
    
                series: [{
                    type: 'area',
                    name: 'Spread',
                    data: chartdata2
                }]
            });
            */
            


            const postdata3 = {};
            postdata3["stock"] = firstsymbol;
    
            console.log(" third post data    ", postdata3);
        
            axios({
                method: 'post',
//                url: 'http://127.0.0.1:8000/info',
                url: '/info',
                data: postdata3,
                headers: {"Content-Type": "application/json"}
              }).then((data3) => {
    
                console.log(" second rawdata   ", data3.data);

                var firststockfundamental = data3.data;

                $("#firststockPEratio").text(firstsymbol.toUpperCase() + "  " + "PE ratio");
                $("#firststockPEratioval").text(firststockfundamental.PEratio);
                $("#firststockPEGratio").text(firstsymbol.toUpperCase() + "  " + "PEG ratio");
                $("#firststockPEGratioval").text(firststockfundamental.PEGratio);
                $("#firststockfuturePEratio").text(firstsymbol.toUpperCase() + "  " + "future PE ratio");
                $("#firststockfuturePEratioval").text(firststockfundamental.futurePEratio);
                $("#firststockfuturePEGratio").text(firstsymbol.toUpperCase() + "  " + "future PEG ratio");
                $("#firststockfuturePEGratioval").text(firststockfundamental.futurePEGratio);
                $("#firststockbeta").text(firstsymbol.toUpperCase() + "  " + "beta");
                $("#firststockbetaval").text(firststockfundamental.beta);

                const postdata4 = {};
                postdata4["stock"] = secondsymbol;

                console.log(" fourth post data   ", postdata4);


                axios({
                  method: 'post',
//                  url: 'http://127.0.0.1:8000/info',
                  url: '/info',
                  data: postdata4,
                  headers: {"Content-Type": "application/json"}
                }).then((data4) => {
      
                  console.log(" second rawdata   ", data4.data);
  
                  var secondstockfundamental = data4.data;
  
                  $("#secondstockPEratio").text(secondsymbol.toUpperCase() + "  " + "PE ratio");
                  $("#secondstockPEratioval").text(secondstockfundamental.PEratio);
                  $("#secondstockPEGratio").text(secondsymbol.toUpperCase() + "  " + "PEG ratio");
                  $("#secondstockPEGratioval").text(secondstockfundamental.PEGratio);
                  $("#secondstockfuturePEratio").text(secondsymbol.toUpperCase() + "  " + "future PE ratio");
                  $("#secondstockfuturePEratioval").text(secondstockfundamental.futurePEratio);
                  $("#secondstockfuturePEGratio").text(secondsymbol.toUpperCase() + "  " + "future PEG ratio");
                  $("#secondstockfuturePEGratioval").text(secondstockfundamental.futurePEGratio);
                  $("#secondstockbeta").text(secondsymbol.toUpperCase() + "  " + "beta");
                  $("#secondstockbetaval").text(secondstockfundamental.beta);


                  function getStandardDeviation (array) {
                    const n = array.length
                    const mean = array.reduce((a, b) => a + b) / n
                    return Math.sqrt(array.map(x => Math.pow(x - mean, 2)).reduce((a, b) => a + b) / n)
                  }


                  //Daily, Weekly, Monthly, Yearly, 5y, 10y
                  var dailyvol = 0.0;
                  var weeklyvol = 0.0;
                  var monthlyvol = 0.0;
                  var yearlyvol = 0.0;
                  var fivevol = 0.0;
                  var tenvol = 0.0;

                  console.log('vols  ', dailyvol, '  ', weeklyvol, '   ', monthlyvol, '   ', yearlyvol, '   ', fivevol, '   ', tenvol);

                  var indexlist = [];
                  var chartdataval = [];
                  for (var i = chartdata.length-1; i >= 0; i--){
                    chartdataval.push(chartdata[i][1]);
                  }
                  
                  try {
                    dailyvol = getStandardDeviation(chartdataval).toFixed(6);
                  }catch(err){
                    console.log(err);
                  }

                  console.log('vols  ', dailyvol, '  ', weeklyvol, '   ', monthlyvol, '   ', yearlyvol, '   ', fivevol, '   ', tenvol);

                  try {
                    indexlist = chartdataval.filter(function(value, index, Arr) {
                      return index % (5) == 0;
                    });
                    weeklyvol = getStandardDeviation(indexlist).toFixed(6);
                  }catch(err){
                    console.log(err);
                  };

                  console.log('vols  ', dailyvol, '  ', weeklyvol, '   ', monthlyvol, '   ', yearlyvol, '   ', fivevol, '   ', tenvol);

                  indexlist = [];
                  try {
                    indexlist = chartdataval.filter(function(value, index, Arr) {
                      return index % (21) == 0;
                    });
                    monthlyvol = getStandardDeviation(indexlist).toFixed(6);
                  }catch(err){
                    console.log(err);
                  };

                  console.log('vols  ', dailyvol, '  ', weeklyvol, '   ', monthlyvol, '   ', yearlyvol, '   ', fivevol, '   ', tenvol);
                  

                  indexlist = [];
                  try {
                    indexlist = chartdataval.filter(function(value, index, Arr) {
                      return index % (252) == 0;
                    });
                    yearlyvol = getStandardDeviation(indexlist).toFixed(6);
                  }catch(err){
                    console.log(err);
                  };
                  
                  console.log('vols  ', dailyvol, '  ', weeklyvol, '   ', monthlyvol, '   ', yearlyvol, '   ', fivevol, '   ', tenvol);
                
                  indexlist = [];
                  try {
                    indexlist = chartdataval.filter(function(value, index, Arr) {
                      return index % (252*5) == 0;
                    });
                    fivevol = getStandardDeviation(indexlist).toFixed(6);
                  }catch(err){
                    console.log(err);
                  };
                  
                  console.log('vols  ', dailyvol, '  ', weeklyvol, '   ', monthlyvol, '   ', yearlyvol, '   ', fivevol, '   ', tenvol);

                  indexlist = [];
                  try {
                    indexlist = chartdataval.filter(function(value, index, Arr) {
                      return index % (252*10) == 0;
                    });
                    tenvol = getStandardDeviation(indexlist).toFixed(6);
                  }catch(err){
                    console.log(err);
                  };

                  console.log('vols  ', dailyvol, '  ', weeklyvol, '   ', monthlyvol, '   ', yearlyvol, '   ', fivevol, '   ', tenvol);

                  $("#spreaddaily").text(dailyvol);
                  $("#spreadweekly").text(weeklyvol);
                  $("#spreadmonthly").text(monthlyvol);
                  $("#spreadyearly").text(yearlyvol);
                  $("#spread5yrs").text(fivevol);
                  $("#spread10yrs").text(tenvol);
                  

                }).catch((err) => {
                  console.log(err);
                })

              }).catch((err) => {
                console.log(err);
              })


            /*
            var cdata = []
            for (var i = 0; i < spreaddate.length; i++){
              var tempcurrdateobj = new Date(spreaddate[i]*1000);
              var tempcurrdateobj2 = new Date(tempcurrdateobj).getTime();
              if (i < 10){
                console.log(" tempcurrdateobj2  ", tempcurrdateobj2);
              }
              cdata.push({time: tempcurrdateobj2/1000, open: spreadopen[i], high: spreadhigh[i], low: spreadlow[i], close: spreadclose[i]});
            }
            console.log(cdata);
            candleSeries.setData(cdata);
            */
          
    
          }).catch((err) => {
            console.log(err);
          });
          
    
      }).catch((err) => {
          console.log(err);
      })

  
  /*
  fetch(`http://127.0.0.1:9665/fetchAPI?endpoint=https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=1000`)
    .then(res => res.json())
    .then(data => {
      const cdata = data.map(d => {
        return {time:d[0]/1000,open:parseFloat(d[1]),high:parseFloat(d[2]),low:parseFloat(d[3]),close:parseFloat(d[4])}
      });
      candleSeries.setData(cdata);
    })
    .catch(err => log(err))

    */
  
      

      /*
    var temp3 = new TradingView.widget({
//    window.tvWidget = new TradingView.widget({
        symbol: 'Spread', // default symbol
        interval: '1d', // default interval
        fullscreen: true, // displays the chart in the fullscreen mode
        container_id: 'tradingview_f6876',
        datafeed: Datafeed,
        library_path: './charting_library/',
//        timezone: "Asia/Seoul",
        timezone: 'Etc/UTC',
        pricescale: 10,
    });
    */
    


      $(".parentchartdiv").show();
    });
  });