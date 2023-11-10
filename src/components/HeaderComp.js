import React from 'react'

const HeaderComp = ({tittleText, descriptionText}) => {
  return (
    <div className="headerComp">
        <div className="chargeTollTxt">
            {tittleText}
        </div>
        <div className="chargeTollTxtLine">

        </div>
        <div className="stepOneMainContent">
            {descriptionText} 
        </div>
    </div>
  )
}

export default HeaderComp