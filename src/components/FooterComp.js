import React from 'react'

const FooterComp = ({previousPageText,nextPageText,previousPage,currentPage,nextPage,error,setError}) => {

    const openPreviousPage = () =>{
        currentPage(false)
        previousPage(true)
    }

    const openNextPage = () =>{
        currentPage(false)
        nextPage(true)
    }

  return (
    <div className="footerContainer">
        {previousPage ? (
            <div className="previousPageButton" onClick={openPreviousPage}>
                {previousPageText}
            </div>
        ) : (
            null
        )}
        {error ? (error) : (null)}
        {nextPage ? (
            <div className="nextPageButton" onClick={openNextPage}>
                {nextPageText}
            </div>
        ) : (
            null
        )}
    </div>
  )
}

export default FooterComp