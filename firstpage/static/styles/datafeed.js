import {
	generateSymbol,
	parseFullSymbol,
} from './helpers.js';
/*
import {
	subscribeOnStream,
	unsubscribeFromStream,
} from './streaming.js';
*/
const lastBarsCache = new Map();

const configurationData = {
//	supported_resolutions: ['1D', '1W', '1M'],

	supported_resolutions: ['1', '2', '3'],
	exchanges: [{
		value: 'Spread',
		name: 'Spread',
		desc: 'Spread',
	},
	{
		// `exchange` argument for the `searchSymbols` method, if a user selects this exchange
		value: 'Spread',

		// filter name
		name: 'Spread',

		// full exchange name displayed in the filter popup
		desc: 'Spread',
	},
	],
	symbols_types: [{
		name: 'Spread',

		// `symbolType` argument for the `searchSymbols` method, if a user selects this symbol type
		value: 'Spread',
	},
		// ...
	],
};

async function getAllSymbols() {
	/*
	const data = await makeApiRequest('data/v3/all/exchanges');
	let allSymbols = [];

	for (const exchange of configurationData.exchanges) {
		const pairs = data.Data[exchange.value].pairs;

		for (const leftPairPart of Object.keys(pairs)) {
			const symbols = pairs[leftPairPart].map(rightPairPart => {
				const symbol = generateSymbol(exchange.value, leftPairPart, rightPairPart);
				return {
					symbol: symbol.short,
					full_name: symbol.full,
					description: symbol.short,
					exchange: exchange.value,
					type: 'crypto',
				};
			});
			allSymbols = [...allSymbols, ...symbols];
		}
	}
	return allSymbols;
	*/

	let allSymbols = [];
	var firstval = {
		description: "GBPAUD",
		exchange: "Oanda",
		full_name: "Oanda:GBPAUD",
		symbol: "GBPAUD",
		type: "crypto",
	}
	allSymbols.push(firstval);
	return allSymbols;

}

export default {
	onReady: (callback) => {
		console.log('[onReady]: Method call');
		setTimeout(() => callback(configurationData));
	},

	searchSymbols: async (
		userInput,
		exchange,
		symbolType,
		onResultReadyCallback,
	) => {
		console.log('[searchSymbols]: Method call');
		const symbols = await getAllSymbols();
		const newSymbols = symbols.filter(symbol => {
			const isExchangeValid = exchange === '' || symbol.exchange === exchange;
			const isFullSymbolContainsInput = symbol.full_name
				.toLowerCase()
				.indexOf(userInput.toLowerCase()) !== -1;
			return isExchangeValid && isFullSymbolContainsInput;
		});
		onResultReadyCallback(newSymbols);
	},

	resolveSymbol: async (
		symbolName,
		onSymbolResolvedCallback,
		onResolveErrorCallback,
	) => {
		console.log('[resolveSymbol]: Method call', symbolName);
		const symbols = await getAllSymbols();
		const symbolItem = symbols.find(({
			full_name,
		}) => full_name === symbolName);
		if (!symbolItem) {
			console.log('[resolveSymbol]: Cannot resolve symbol', symbolName);
			onResolveErrorCallback('cannot resolve symbol');
			return;
		}
		const symbolInfo = {
			name: symbolItem.symbol,
			description: symbolItem.description,
			type: symbolItem.type,
			session: '24x7',
//			timezone: 'Etc/UTC',
//			timezone: 'UTC+9',
			timezone: 'Asia/Seoul',
//			timezone: 'Etc/UTC',
			exchange: symbolItem.exchange,
			minmov: 1,
			pricescale: 100000,
			has_intraday: true,
			has_no_volume: true,
			has_weekly_and_monthly: false,
			supported_resolutions: configurationData.supported_resolutions,
			volume_precision: 2,
			data_status: 'streaming',
		};

		console.log('[resolveSymbol]: Symbol resolved', symbolName);
		onSymbolResolvedCallback(symbolInfo);
	},

	getBars: async (symbolInfo, resolution, from, to, onHistoryCallback, onErrorCallback, firstDataRequest) => {


		var currdata = [];
		var resp = await axios.get("http://127.0.0.1:3000/GBPAUD");
		if (resp.status == 200){
			var currdata2 = resp.data;
			var ohlcs = currdata2.ohlcs;
			var timestamps = currdata2.ts;
			for (var i = 0; i < ohlcs.length; i++){
				if (i == ohlcs.length-1){
					var temp = {
						close: parseFloat(ohlcs[i].c),
						high: parseFloat(ohlcs[i].h),
						isBarClosed: true,
						isLastBar: true,
						low: parseFloat(ohlcs[i].l),
						open: parseFloat(ohlcs[i].o),
						time: timestamps[i]*1000,
					}
					currdata.push(temp);
				}else{
					var temp = {
						close: parseFloat(ohlcs[i].c),
						high: parseFloat(ohlcs[i].h),
						isBarClosed: true,
						isLastBar: false,
						low: parseFloat(ohlcs[i].l),
						open: parseFloat(ohlcs[i].o),
						time: timestamps[i]*1000,
					}
					currdata.push(temp);
				}

			}
		};


		/*
		const url = "https://min-api.cryptocompare.com/data/v2/histominute?fsym=GBP&tsym=AUD&limit=1000&api_key=f7805a6e014ff82c897176c34005c3af8ca1412f7e923f7d4420c4513d6e2abc"
		let currdata = [];
		var resp = await axios.get(url);
			if (resp.status == 200){
				var currdata2 = resp.data.Data.Data;
				for (var i = 0; i < currdata2.length; i++){
					if (i != currdata2.length - 1){
						var temp = {
							close: currdata2[i].close,
							high: currdata2[i].high,
							isBarClosed: true,
							isLastBar: false,
							low: currdata2[i].low,
							open: currdata2[i].open,
							time: currdata2[i].time * 1000,
						}
						currdata.push(temp);
					}
					if (i == currdata2.length -1 ){
						var temp = {
							close: currdata2[i].close,
							high: currdata2[i].high,
							isBarClosed: true,
							isLastBar: true,
							low: currdata2[i].low,
							open: currdata2[i].open,
							time: currdata2[i].time * 1000,
						}
						currdata.push(temp);
					}
				}
			}
			*/
//		}).catch(error => {
//			console.log(error);
//		});
		console.log(" ============================================== ");
		console.log(currdata);
		console.log("=================================================== ");
		onHistoryCallback(currdata, {
			noData: false,
		});
	},

    /*
	subscribeBars: (
		symbolInfo,
		resolution,
		onRealtimeCallback,
		subscribeUID,
		onResetCacheNeededCallback,
	) => {


		axios.get("http://127.0.0.1:3000/GBPAUD").then((resp) => {
			var currdata = [];
			if (resp.status == 200){
				var currdata2 = resp.data;
				var ohlcs = currdata2.ohlcs;
				var timestamps = currdata2.ts;
				for (var i = 0; i < ohlcs.length; i++){
					if (i == ohlcs.length-1){
						var temp = {
							close: parseFloat(ohlcs[i].c),
							high: parseFloat(ohlcs[i].h),
							isBarClosed: true,
							isLastBar: true,
							low: parseFloat(ohlcs[i].l),
							open: parseFloat(ohlcs[i].o),
							time: timestamps[i]*1000,
						}
						currdata.push(temp);
					}else{
						var temp = {
							close: parseFloat(ohlcs[i].c),
							high: parseFloat(ohlcs[i].h),
							isBarClosed: true,
							isLastBar: false,
							low: parseFloat(ohlcs[i].l),
							open: parseFloat(ohlcs[i].o),
							time: timestamps[i]*1000,
						}
						currdata.push(temp);
					}
	
				}
			};
			var lastBarcache = currdata[currdata.length-1];
			console.log('[subscribeBars]: Method call with subscribeUID:', subscribeUID);
			subscribeOnStream(
				symbolInfo,
				resolution,
				onRealtimeCallback,
				subscribeUID,
				onResetCacheNeededCallback,
	//			lastBarsCache.get(symbolInfo.full_name),
				lastBarcache,
				
			);
		})



		/*
		const url = "https://min-api.cryptocompare.com/data/v2/histominute?fsym=GBP&tsym=AUD&limit=10&api_key=f7805a6e014ff82c897176c34005c3af8ca1412f7e923f7d4420c4513d6e2abc";

		axios.get(url).then((resp) => {
			var currdata = [];
			if (resp.status == 200){
				var currdata2 = resp.data.Data.Data;
				for (var i = 0; i < currdata2.length; i++){
					if (i != currdata2.length - 1){
						var temp = {
							close: currdata2[i].close,
							high: currdata2[i].high,
							isBarClosed: true,
							isLastBar: false,
							low: currdata2[i].low,
							open: currdata2[i].open,
							time: currdata2[i].time * 1000,
						}
						currdata.push(temp);
					}
					if (i == currdata2.length -1 ){
						var temp = {
							close: currdata2[i].close,
							high: currdata2[i].high,
							isBarClosed: true,
							isLastBar: true,
							low: currdata2[i].low,
							open: currdata2[i].open,
							time: currdata2[i].time * 1000,
						}
						currdata.push(temp);
					}
				}
			}
			var lastBarcache = currdata[currdata.length-1];
			console.log('[subscribeBars]: Method call with subscribeUID:', subscribeUID);
			subscribeOnStream(
				symbolInfo,
				resolution,
				onRealtimeCallback,
				subscribeUID,
				onResetCacheNeededCallback,
	//			lastBarsCache.get(symbolInfo.full_name),
				lastBarcache,
				
			);
		});

		console.log('[subscribeBars]: Method call with subscribeUID:', subscribeUID);
		subscribeOnStream(
			symbolInfo,
			resolution,
			onRealtimeCallback,
			subscribeUID,
			onResetCacheNeededCallback,
//			lastBarsCache.get(symbolInfo.full_name),
			lastBarcache,
			
		);
		
    },
    

	unsubscribeBars: (subscriberUID) => {
		console.log('[unsubscribeBars]: Method call with subscriberUID:', subscriberUID);
		unsubscribeFromStream(subscriberUID);
    },
    */
};