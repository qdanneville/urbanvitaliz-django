describe('I can read only project state', () => {

    beforeEach(() => {
        cy.login("jeanne");
    })

    it('goes to project state and read only content', () => {

        cy.visit('/projects')

        cy.contains('Friche numéro 1').click({force:true});

        cy.contains("État des lieux").click({ force: true })

        cy.url().should('include', '/connaissance')

        cy.contains("Compléter cette section").should('not.exist')
    })
})
