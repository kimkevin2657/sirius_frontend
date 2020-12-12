/*
// Make requests to CryptoCompare API
export async function makeApiRequest(path) {
//export async function makeApiRequest(path) {
	try {
		const response = await fetch(`https://min-api.cryptocompare.com/${path}`);
		return response.json();
	} catch (error) {
		throw new Error(`CryptoCompare request error: ${error.status}`);
	}
}
export async function currentpriceBTCUSD(){
	try{
		const response = await fetch("https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD&api_key=f7805a6e014ff82c897176c34005c3af8ca1412f7e923f7d4420c4513d6e2abc")
		return response.json();
	}catch(error){
		throw new Error('CryptoCompare currentprice request error: ${error.status}')
	}

}
*/
// Generate a symbol ID from a pair of the coins
export function generateSymbol(exchange, fromSymbol, toSymbol) {
//export function generateSymbol(exchange, fromSymbol, toSymbol) {
	const short = `${fromSymbol}/${toSymbol}`;
	return {
		short,
		full: `${exchange}:${short}`,
	};
}

export function parseFullSymbol(fullSymbol){
//export function parseFullSymbol(fullSymbol) {
	const match = fullSymbol.match(/^(\w+):(\w+)\/(\w+)$/);
	if (!match) {
		return null;
	}

	return {
		exchange: match[1],
		fromSymbol: match[2],
		toSymbol: match[3],
	};
}