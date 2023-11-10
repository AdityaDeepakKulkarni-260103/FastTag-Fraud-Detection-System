import React from 'react'
import HeaderComp from './HeaderComp'

const StepTwoB = ({stepTwoBOpen}) => {
    if (stepTwoBOpen) {
        return (
            <div className="stepContainer">
                <HeaderComp tittleText={"Select Option"} descriptionText={"Select method to charge toll"} />
                <div className="stepOneContent">

                </div>
            </div>
          )   
    } else {
        return(null)
    }
}

export default StepTwoB