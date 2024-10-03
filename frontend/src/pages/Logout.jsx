import React from 'react'
import { useEffect } from 'react'

const Logout = () => {

    useEffect(() =>  {
    localStorage.removeItem("access_token");
    console.log("User logged out successfully");
}, []);


  return (
    <div className="w-4/5 mx-auto flex flex-row justify-center items-center mt-[2rem]">
      <div className="bg-white shadow-md border border-gray-200 rounded-lg w-[30rem] p-4 sm:p-6 lg:p-8 slide-right fade-in">
        <form className="space-y-6" action="#">
      <h3 className="text-xl font-medium text-gray-500 pb-10px">You're Signed out!</h3>
      <p className='text-gray-500 pb-[1rem]'>You can sign in to enable features of Notifications</p>
      <a href="/login" >
              <button
                type="button"
                className="w-[25rem] flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-500 hover:bg-green-600"
              >
                Sign In
              </button>
                </a>

          </form>
    </div>
    </div>
  )
}

export default Logout
