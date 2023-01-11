function MeasurementTable({ data, isLoading, ...props }) {

    if (isLoading) {
        return <div>
            Loading...
        </div>
    }

    return <div>
        <div>
            <tr>
                <th> ID </th>
                <th> Measurement </th>
                <th> Value </th>
                <th> Timestamp </th>
                <th> apid </th>
            </tr>
            {data.map((item) => {
                return <tr key={item._id}>
                    <td> {item._id} </td>
                    <td> {item.measurement} </td>
                    <td> {item.value} </td>
                    <td> {item.time} </td>
                    <td> {item.apid} </td>
                </tr>
            })}
        </div>
    </div>
}

export default MeasurementTable;
