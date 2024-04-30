describe('cypress tests', () => {
  it('renders home page', () => {
    cy.visit('http://localhost:3000')
    cy.get('[data-testid="cypress-test-button"]').should('exist')
    .should('have.text', 'Login with Spotify')
  })

  it('get top Artist button works', () => {
    cy.visit('http://localhost:3000/dashboard?user_id=31d4tpb5akuckk3k2i6yazjglnaq')
    cy.get('[data-testid="cypress-gettopArtist"]').should('exist')
    .should('have.text', 'Show Top Artists')
  
  })

  it('click top Artist button 4 weeks works', () => {
    cy.visit('http://localhost:3000/dashboard?user_id=31d4tpb5akuckk3k2i6yazjglnaq')
    cy.get('[data-testid="cypress-gettopArtist"]').click()
    cy.get('[data-testid="cypress-gettopArtist4weeks"]').should('exist')
    cy.get('[data-testid="cypress-gettopArtist4weeks"]').click()
    cy.wait(1000)
    cy.get('[data-testId="cypress-topArtist-Image"]').should('exist')
    .should('have.text', 'Image')
    cy.get('[data-testId="cypress-topArtist-ArtistName"]').should('exist')
    .should('have.text', 'Artist Name')
    cy.get('[data-testId="cypress-topArtist-ID"]').should('exist')
    .should('have.text', 'ID')
    cy.get('[data-testId="cypress-topArtist-Table"]').should('exist')
    
  })

  it('click top Artist button 6 months works', () => {
    cy.visit('http://localhost:3000/dashboard?user_id=31d4tpb5akuckk3k2i6yazjglnaq')
    cy.get('[data-testid="cypress-gettopArtist"]').click()
    cy.get('[data-testid="cypress-gettopArtist6months"]').should('exist')
    cy.get('[data-testid="cypress-gettopArtist6months"]').click()
    cy.wait(1000)
    cy.get('[data-testId="cypress-topArtist-Image"]').should('exist')
    .should('have.text', 'Image')
    cy.get('[data-testId="cypress-topArtist-ArtistName"]').should('exist')
    .should('have.text', 'Artist Name')
    cy.get('[data-testId="cypress-topArtist-ID"]').should('exist')
    .should('have.text', 'ID')
    cy.get('[data-testId="cypress-topArtist-Table"]').should('exist')
    
  })

  it('click top Artist button 12 months works', () => {
    cy.visit('http://localhost:3000/dashboard?user_id=31d4tpb5akuckk3k2i6yazjglnaq')
    cy.get('[data-testid="cypress-gettopArtist"]').click()
    cy.get('[data-testid="cypress-gettopArtist12months"]').should('exist')
    cy.get('[data-testid="cypress-gettopArtist12months"]').click()
    cy.wait(1000)
    cy.get('[data-testId="cypress-topArtist-Image"]').should('exist')
    .should('have.text', 'Image')
    cy.get('[data-testId="cypress-topArtist-ArtistName"]').should('exist')
    .should('have.text', 'Artist Name')
    cy.get('[data-testId="cypress-topArtist-ID"]').should('exist')
    .should('have.text', 'ID')
    cy.get('[data-testId="cypress-topArtist-Table"]').should('exist')
  })

  // it('get top artist button works', () => {
  //   cy.visit('http://localhost:3000/dashboard')
  //   cy.get('[data-testid="cypress-gettopArtist"]').should('exist')
  //   .should('have.text', 'Show Top Artists')
  // })
})