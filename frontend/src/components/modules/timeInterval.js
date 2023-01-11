import React, { useEffect, useState, useRef } from 'react'

function TimeInterval ({ intervalStart }) {
    const intervalFunction = useRef(null)
    const [secondsSinceUpdate, setSecondsSinceUpdate] = useState(0)

    const updateInterval = () => {
        const date = new Date()
        const timeDiff = date - intervalStart
        setSecondsSinceUpdate(Math.floor(timeDiff / 1000))
    }

    useEffect(() => {
        // Update interval function when lastUpdate changes
        // Required because interval closure does not include react state
        updateInterval()
        intervalFunction.current = () => {
            updateInterval()
        }
    }, [intervalStart])

    useEffect(() => {
        const interval = setInterval(() => intervalFunction.current(), 1 * 1000)
        return () => clearInterval(interval)
    }, [])

    const seconds2str = (seconds_interval) => {
        const minutes = Math.floor(seconds_interval / 60)
        const seconds = seconds_interval % 60
        if (minutes === 0) {
            return `${seconds} seconds`
        }
        if (seconds === 0) {
            return `${minutes} minutes`
        }
        return `${minutes} minutes ${seconds} seconds`
    }

    return <div>
        Time since last update: {seconds2str(secondsSinceUpdate)}
    </div>
}

export default TimeInterval;
