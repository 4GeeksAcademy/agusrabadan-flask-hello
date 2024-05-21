import React from 'react'

export const UserProfile = ({username, email, bio}) => {
  return (
    <div className="card">
      <div className="card-body">
        <h5 className="card-title">Card title</h5>
        <div className="user-profile-container">
          <div className="user-profile">
            <h2 className="profile-title">Perfil de Usuario</h2>
            <div className="profile-details">
              <p><strong>Nombre de usuario:</strong> {username}</p>
              <p><strong>Email:</strong> {email}</p>
              <p><strong>Bio:</strong> {bio}</p>
            </div>
          </div>
        </div>
      </div>
      <img src="data:image/png;base64,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" className="card-img-bottom" alt="My profile" />
    </div>
  )
}
