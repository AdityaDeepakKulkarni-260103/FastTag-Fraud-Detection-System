import React, { useEffect, useState } from 'react'
import HeaderComp from './HeaderComp'
import VehicleDetail from './VehicleDetail'
import FooterComp from './FooterComp'

const StepFourS = ({setImage,image,setStepOneOpen,setStepTwoAOpen,stepFourSOpen,setStepFourSOpen,vehicleDetails,setError,error}) => {

    if (stepFourSOpen && vehicleDetails) {
        return (
            <div className="stepContainer">
                <HeaderComp tittleText={"Vehicle Details"} descriptionText={"Owner was charged rs. 50"} />
                <div className="finalContent">
                    <div className="vehicleDetails">
                        <VehicleDetail vehicleDetailsLabel={"Registration Number"} vehicleDetailsvalue={vehicleDetails.CarRegistration} />
                        <VehicleDetail vehicleDetailsLabel={"Owner Name"} vehicleDetailsvalue={vehicleDetails.Username} />
                        <VehicleDetail vehicleDetailsLabel={"New Balance"} vehicleDetailsvalue={'₹'+vehicleDetails.AccountBalance} />
                        <VehicleDetail vehicleDetailsLabel={"Vehicle Make"} vehicleDetailsvalue={vehicleDetails.CarMake} />
                        <VehicleDetail vehicleDetailsLabel={"Vehicle Model"} vehicleDetailsvalue={vehicleDetails.CarModel} />
                        <VehicleDetail vehicleDetailsLabel={"Vehicle Color"} vehicleDetailsvalue={vehicleDetails.CarColour} />
                    </div>
                    <div className="vehicleImage">
                        <img src={image} alt="" />
                    </div>
                </div>
                <FooterComp error={error} setError={setError} previousPageText={"Go Back"} nextPageText={"New Scan"} previousPage={setStepTwoAOpen} currentPage={setStepFourSOpen} nextPage={setStepOneOpen} />
            </div>
          )
    } else {
        return (
            null
          )
    }
}

export default StepFourS