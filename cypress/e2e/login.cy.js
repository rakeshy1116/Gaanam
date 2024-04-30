describe('OAuth Tests', () => {
    it('Visits Spotify Authorization Page', () => {
        cy.visit('https://accounts.spotify.com/authorize');
    });
    // it('Visits Spotify', () => {
    //     it('Lol', () => {
    //       cy.visit('https://accounts.spotify.com/en/login')
    //       cy.get('input#login-username').click().type(Cypress.env('SPOTIFY_USERNAME'))
    //       cy.get('input#login-password').click().type(Cypress.env('SPOTIFY_PASSWORD'))
    //       cy.get('#login-button').click()
    //     })
    //   })
    // it('Logs In to Spotify', () => {

    // });
    // it('Handles Redirect and Obtains Token', () => {
    //     // Handle redirect URI after successful authentication
    //     cy.url().then(url => {
    //         // Extract access token from URL or response
    //         const accessToken = extractTokenFromUrl(url);
    //         // Use the token for further API requests
    //         // For example, set it in local storage or as a cookie
    //         cy.wrap(accessToken).as('accessToken'); // Alias the accessToken
    //     });
    // });

    // it('Tests API with Access Token', () => {
    //     // Make API requests to Spotify API using the access token
    //     cy.get('@accessToken').then(accessToken => { // Use the aliased accessToken
    //         cy.request({
    //             method: 'GET',
    //             url: 'https://api.spotify.com/v1/me',
    //             headers: {
    //                 'Authorization': `Bearer ${accessToken}`
    //             }
    //         }).then(response => {
    //             // Assert response as per your requirements
    //             expect(response.status).to.equal(200);
    //         });
    //     });
    // });
});