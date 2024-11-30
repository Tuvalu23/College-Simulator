# University Admissions Simulator

A Flask-based web application that simulates the admissions process for multiple universities. Users can select a university, log in through a simple interface, check their application status, and receive a randomly determined decision of either acceptance or rejection.

## To-Do
- [X] UChicago
- [X] Harvard
- [X] MIT
- [ ] Stanford
- [ ] Yale 

## Features

### University Selection
- **Dynamic List**: Users can choose from a list of universities displayed with their logos.
- **New Tab Navigation**: Each university's login page opens in a new tab for seamless navigation.

### Login Page
- **Custom Login**: Users enter credentials specific to each selected university.

### Status Simulation
- **Random Decision**: Users receive either an acceptance or rejection result with a 50% chance.
- **Detailed Status Updates**: Custom status pages display personalized messages and application details.

### Custom Static Assets
- Each university has dedicated assets, including logos, CSS, and JavaScript files, for a unique and branded user experience.

### Responsive Design
- **Modern Layout**: The application uses a responsive grid layout, ensuring compatibility across devices.

## Technologies Used

### Backend
- **Python**: Flask framework for server-side logic and routing.

### Frontend
- **HTML/CSS**: Custom templates styled for each university.
- **Tailwind CSS**: For responsive and modern design elements.

### Additional Features
- **Random Module**: Used for decision-making.
- **Dynamic Templating**: Flask's `url_for` dynamically links resources and pages.
