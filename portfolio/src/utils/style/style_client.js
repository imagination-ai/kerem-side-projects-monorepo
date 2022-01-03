import axios from 'axios'

export default class StyleClient {
  constructor (host, port) {
    this.host = host
    if (!host.startsWith("http")) {
      this.host = "http://" + host
    }
    this.port = port
    this.base_url = `${this.host}:${this.port}/api/v1`
    console.log('Base URL for StyleClient ' + this.base_url)
  }

  predict = async (text, model_name) => {
    const url = this.base_url + '/Predictions/predict'
    let data = { text: text, model_name: model_name } 

    // axios
    //   .post(url, data, {
    //     headers: {
    //       'content-type': 'application/json'
    //     }
    //   })
    //   .then(response => {
    //     predictionSetter(response)
    //   })
    const results = await axios.post(url, data);
    return results;
    // console.log('Predictions: ' + JSON.stringify(preds))
    // return preds.data;
  }
}
