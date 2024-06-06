import React, { useContext } from "react";
import { Context } from "../store/appContext.js";


export const Profile = () => {
  const {store } = useContext(Context)
  

  return (
    <div className="container">
      <p className="text-success">
        Me cago en dios
      </p>
    </div>
  )
}