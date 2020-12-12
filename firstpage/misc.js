
const axios = require("axios");


/*
axios.post('http://127.0.0.1:5050/historical', postdata).then((data) => {
  console.log(data);
})  .catch(error => {
    console.log(error);
  });
*/

const postdata = {};
postdata["stock"] = 'aapl';
postdata['period'] = 'max';
postdata['interval'] = '1d';

axios({
  method: 'post',
  url: 'http://127.0.0.1:5050/historical',
  data: postdata,
  headers: {"Content-Type": "application/json"}
}).then((data) => {


    firstdata = [];
    firstdataopen = [];
    firstdatahigh = [];
    firstdatalow = [];
    firstdataclose = [];
    for (var i = data.data.date.length; i > 0; i--){
        firstdata.push(data.data.date[i]);
        firstdataopen.push(data.data.open[i]);
        firstdatahigh.push(data.data.high[i]);
        firstdatalow.push(data.data.low[i]);
        firstdataclose.push(data.data.close[i]);
        if (firstdata.length >= 365){
            break;
        }
    }
    firstdata.reverse();
    firstdataopen.reverse();
    firstdatahigh.reverse();
    firstdatalow.reverse();
    firstdataclose.reverse();


    const postdata2 = {};
    postdata2["stock"] = 'fb';
    postdata2['period'] = 'max';
    postdata2['interval'] = '1d';

    axios({
        method: 'post',
        url: 'http://127.0.0.1:5050/historical',
        data: postdata2,
        headers: {"Content-Type": "application/json"}
      }).then((data2) => {

        seconddata = [];
        seconddataopen = [];
        seconddatahigh = [];
        seconddatalow = [];
        seconddataclose = [];
        for (var i = data2.data.date.length; i > 0; i--){
            seconddata.push(data2.data.date[i]);
            seconddataopen.push(data2.data.open[i]);
            seconddatahigh.push(data2.data.high[i]);
            seconddatalow.push(data2.data.low[i]);
            seconddataclose.push(data2.data.close[i]);
            if (seconddata.length >= 365){
                break;
            }
        }
        seconddata.reverse();
        seconddataopen.reverse();
        seconddatahigh.reverse();
        seconddatalow.reverse();
        seconddataclose.reverse();

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

        }
        console.log(spreadopen);
        

      }).catch((err) => {
        console.log(err);
      });
      

  }).catch((err) => {
      console.log(err);
  })

/*
axios.get("http://127.0.0.1:5050/historicaltest").then((data) => {
    console.log(data);
})
*/