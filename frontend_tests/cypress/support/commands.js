import users from '../fixtures/users/users.json'

console.log('users : ', users[4].fields.username);

Cypress.Commands.add("login", (role) => {

    let username = ""

    switch (role) {
        case "jean":
            username = users[1].fields.username
            break;
        case "jeanne":
            username = users[2].fields.username
            break;
        case "jeannot":
            username = users[3].fields.username
            break;
        case "bob":
            username = users[4].fields.username
            break;
        case "boba":
            username = users[5].fields.username
            break;
        case "bobette":
            username = users[6].fields.username
            break;
        case "staff":
            username = users[0].fields.username
            break;
        default:
            break;
    }

    cy.request({ url: "/accounts/login/" }).then(response => {
        const setCookieValue = response.headers["set-cookie"][0]

        const regExp = /\=([^=]+)\;/;
        const matches = regExp.exec(setCookieValue);
        const token = matches[1]

        cy.request({
            method: "POST",
            url: "/accounts/login/",
            form: true,
            body: {
                login: username,
                password: "derpderp",
                csrfmiddlewaretoken: token
            }
        }).then(response => {
            cy.getCookie("sessionid").should("exist");
            cy.getCookie("csrftoken").should("exist");
        })
    })
})
