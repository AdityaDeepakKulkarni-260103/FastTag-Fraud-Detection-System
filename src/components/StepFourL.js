import React, { useEffect, useState } from 'react'
import HeaderComp from './HeaderComp'
import VehicleDetail from './VehicleDetail'
import FooterComp from './FooterComp'

const StepFourL = ({setStepOneOpen,setStepTwoAOpen,stepFourLOpen,setStepFourLOpen,vehicleDetails,setError,error}) => {

    if (stepFourLOpen && vehicleDetails) {

        console.log(vehicleDetails);
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
                </div>
                <FooterComp error={error} setError={setError} previousPageText={"Go Back"} nextPageText={"New Scan"} previousPage={setStepTwoAOpen} currentPage={setStepFourLOpen} nextPage={setStepOneOpen} />
            </div>
          )
    } else {
        return (
            null
          )
    }
}

export default StepFourL