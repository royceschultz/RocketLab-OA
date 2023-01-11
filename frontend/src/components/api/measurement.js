class MeasurementAPI {
    constructor() {
        this.url = 'http://localhost:5000';
    }
    
    async lookup(measurement, page) {
        const response = await fetch(this.url + `/measurement/lookup?measurement=${measurement}&page=${page}`);
        const data = await response.json();
        return data;
    }

    async load_mock_data() {
        const response = await fetch(this.url + '/dev/load_mock_data');
    }

    async drop_table() {
        const response = await fetch(this.url + '/dev/drop_table');
    }
}

const measurementAPI = new MeasurementAPI()

export default measurementAPI
