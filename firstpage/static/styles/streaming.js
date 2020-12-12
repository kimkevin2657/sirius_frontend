import { parseFullSymbol } from './helpers.js';

//var apiKey = "f7805a6e014ff82c897176c34005c3af8ca1412f7e923f7d4420c4513d6e2abc";
//const socket = io('wss://streamer.cryptocompare.com');
//const socket = io('wss://streamer.cryptocompare.com/v2?api_key=' + apiKey);
const socket = io("ws://127.0.0.1:5001");

const channelToSubscription = new Map();

var boolean_count = 0;


socket.on('connect', () => {
	boolean_count = 0
	console.log('[socket] Connected');
});

socket.on('disconnect', (reason) => {
	console.log('[socket] Disconnected:', reason);
});

socket.on('error', (error) => {
	console.log('[socket] Error:', error);
});

socket.on('message', data => {
	console.log('[socket] Message:', data);
	/*
	const [
		eventTypeStr,
		exchange,
		fromSymbol,
		toSymbol,
		,
		,
		tradeTimeStr,
		,
		tradePriceStr,
	] = data.split('~');
	

	console.log(" ======= ");
	console.log(eventTypeStr);
	console.log(exchange);
	console.log(fromSymbol);
	console.log(toSymbol);
	console.log(tradeTimeStr);
	console.log(tradePriceStr);
	console.log(" ======= ");
	*/
	const eventTypeStr = '0';
	const exchange = 'Oanda';
	const fromSymbol = 'GBP'; 
	const toSymbol = 'AUD';
	const tradeTimeStr = data.t;
	const tradePriceStr = data.p;

	// var tradePriceStr = data.P;
	// var tradeTimeStr = data.TS; // this timestamp will be in seconds

	if (parseInt(eventTypeStr) !== 0) {
		// skip all non-TRADE events
		return;
	}
	const tradePrice = parseFloat(tradePriceStr);
	var tradeTime = parseInt(tradeTimeStr);
	//////////////////
	if (tradeTime.toString().length == 10){
		tradeTime *= 1000;
	}
	///////////////////
	const channelString = `0~${exchange}~${fromSymbol}~${toSymbol}`;
	const subscriptionItem = channelToSubscription.get(channelString);
	if (subscriptionItem === undefined) {
		return;
	}
	/*
	if (boolean_count == 0){
		let tempdate;
		if (tradeTime.toString().length == 10){
			tempdate = new Date(tradeTime*1000);
		};
		if (tradeTime.toString().length == 13){
			tempdate = new Date(tradeTime); 
		};
//		let tempdate = new Date(tradeTime*1000);
		let secs = tempdate.getSeconds();
		let temptradeTime = tradeTime - secs*1000;
		subscriptionItem.lastDailyBar.time = temptradeTime;
		boolean_count += 1;

	} 
	*/
	const lastDailyBar = subscriptionItem.lastDailyBar;
	const nextDailyBarTime = getNextDailyBarTime(lastDailyBar.time);

	let bar;
	if (tradeTime >= nextDailyBarTime) {
		bar = {
			time: nextDailyBarTime,
			open: tradePrice,
			high: tradePrice,
			low: tradePrice,
			close: tradePrice,
		};
		console.log('[socket] Generate new bar', bar);
	} else {
		bar = {
			...lastDailyBar,
			high: Math.max(lastDailyBar.high, tradePrice),
			low: Math.min(lastDailyBar.low, tradePrice),
			close: tradePrice,
		};
		console.log('[socket] Update the latest bar by price', tradePrice);
	}
	subscriptionItem.lastDailyBar = bar;

	// send data to every subscriber of that symbol
	subscriptionItem.handlers.forEach(handler => handler.callback(bar));
});

function getNextDailyBarTime(barTime) {
	/*
	const date = new Date(barTime * 1000);
	date.setDate(date.getDate() + 1);
	return date.getTime() / 1000;
	*/
	/*
	const date = new Date(barTime * 1000);
	date.setMinutes(date.getMinutes() + 1);
	return date.getTime()/1000;
	*/
	if (parseInt(barTime).toString().length == 10){
		return (parseInt(barTime) + 60)*1000;
	};
	if (parseInt(barTime).toString().length == 13){
		return parseInt(barTime) + 60000;

	};
}



export function subscribeOnStream(
	symbolInfo,
	resolution,
	onRealtimeCallback,
	subscribeUID,
	onResetCacheNeededCallback,
	lastDailyBar,
) {
	console.log(" symbolInfo data at subscribeOnStream   ", symbolInfo);
	console.log(" symbolInfo.full_name at subscribeOnStream   ", symbolInfo.full_name);
//	const parsedSymbol = parseFullSymbol(symbolInfo.full_name);
	var parsedSymbolExchange = "Oanda";
	var parsedSymbolfromSymbol = "GBP";
	var parsedSymboltoSymbol = "AUD";
	const channelString = `0~${parsedSymbolExchange}~${parsedSymbolfromSymbol}~${parsedSymboltoSymbol}`;
	const handler = {
		id: subscribeUID,
		callback: onRealtimeCallback,
	};
	let subscriptionItem = channelToSubscription.get(channelString);
	if (subscriptionItem) {
		// already subscribed to the channel, use the existing subscription
		subscriptionItem.handlers.push(handler);
		return;
	}
	subscriptionItem = {
		subscribeUID,
		resolution,
		lastDailyBar,
		handlers: [handler],
	};
	channelToSubscription.set(channelString, subscriptionItem);
	console.log('[subscribeBars]: Subscribe to streaming. Channel:', channelString);
	socket.emit('SubAdd', { subs: [channelString] });
}

export function unsubscribeFromStream(subscriberUID) {
	// find a subscription with id === subscriberUID
	for (const channelString of channelToSubscription.keys()) {
		const subscriptionItem = channelToSubscription.get(channelString);
		const handlerIndex = subscriptionItem.handlers
			.findIndex(handler => handler.id === subscriberUID);

		if (handlerIndex !== -1) {
			// remove from handlers
			subscriptionItem.handlers.splice(handlerIndex, 1);

			if (subscriptionItem.handlers.length === 0) {
				// unsubscribe from the channel, if it was the last handler
				console.log('[unsubscribeBars]: Unsubscribe from streaming. Channel:', channelString);
				socket.emit('SubRemove', { subs: [channelString] });
				channelToSubscription.delete(channelString);
				break;
			}
		}
	}
}
