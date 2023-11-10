import React from 'react'
import HeaderComp from './HeaderComp'

const StepThreeA = ({stepThreeAOpen,setStepThreeAOpen}) => {
    if (stepThreeAOpen) {
        return (
            <div className="stepContainer">
                <HeaderComp tittleText={"Image Upload"} descriptionText={"Check uploaded image"} />
            </div>
          )
    } else {
        return (
            null
          )
    }
}

export default StepThreeA