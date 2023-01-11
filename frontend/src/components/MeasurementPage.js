import React, { useState, useEffect } from 'react'
import measurementAPI from './api/measurement.js'

import PageSelector from './modules/pageSelector.js'
import TimeInterval from './modules/timeInterval.js'
import MeasurementTable from './modules/measurementTable.js'
import DevButtons from './modules/devButtons.js'

function MeasurementPage() {
    const [data, setData] = useState([])
    const [isLoading, setIsLoading] = useState(true)
    const [lastUpdate, setLastUpdate] = useState(null)
    const [page, setPage] = useState(1)

    const [search, setSearch] = useState('')

    async function fetchData() {
        setIsLoading(true)
        const data = await measurementAPI.lookup(search, page)
        setData(data.results)
        setIsLoading(false)
        setLastUpdate(new Date())
    }

    useEffect(() => {
        fetchData()
    }, [search, page])

    const handleSearch = (event) => {
        setSearch(event.target.value)
        console.log(event.target.value)
    }

    return <div>
        <form onSubmit={(e) => {e.preventDefault()}}>
            <label>
                Search Measurements (Regex):
                <input type='text' name='search' value={search} onChange={handleSearch}/>
            </label>
        </form>
        <PageSelector page={page} setPage={setPage} />
        <div>
            <button onClick={() => {
                setPage(1)
                setData([])
            }}>
                Reset
            </button>
            <button onClick={fetchData}>
                Fetch
            </button>
        </div>
        <DevButtons refresh={fetchData} />
        <TimeInterval intervalStart={lastUpdate} />
        <MeasurementTable data={data} isLoading={isLoading}/>
    </div>
}

export default MeasurementPage;
