import React from 'react'

const VehicleDetail = ({vehicleDetailsLabel,vehicleDetailsvalue}) => {
  return (
        <div className="vehicleDetailsContainer">
            <div className="vehicleDetailsLabels">
                {vehicleDetailsLabel}
            </div>
            <div className="vehicleDetailsvalues">
                {vehicleDetailsvalue}
            </div>
        </div>
    )
}

export default VehicleDetail