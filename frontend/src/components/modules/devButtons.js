import measurementAPI from "../api/measurement"

function DevButtons ({refresh, ...props}) {
    return <div>
        <button onClick={async () => {
            await measurementAPI.load_mock_data()
            refresh()
        }}>
            Add Mock Data
        </button>
        <button onClick={async () => {
            await measurementAPI.drop_table()
            refresh()
        }}>
            Drop Table
        </button>
    </div>
}

export default DevButtons
