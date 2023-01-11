function PageSelector({page, setPage, ...props}) {
    return <div>
        <button onClick={() => {
            if (page > 1) {
                setPage(page - 1)
            }
        }}>
            Previous Page
        </button>
        <button>
            Current Page: {page}
        </button>
        <button onClick={() => {
            setPage(page + 1)
        }}>
            Next Page
        </button>
    </div>
}

export default PageSelector;
