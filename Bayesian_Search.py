import numpy as np
np.random.seed(999)

def generate_2D_space(size):
    # generate 2D rectangula space
    space = np.zeros((size, size))
    return space

def mark_true_position(space):
    x_pos = np.random.randint(low=0, high=10, size=1) # low in; high ex
    y_pos = np.random.randint(low=0, high=10, size=1)
    x_pos = int(x_pos)
    y_pos = int(y_pos)
    space[x_pos][y_pos] = 1
    return space

def flatten_space(space):
    f_space = space.reshape((x_size*x_size, ))
    return f_space

def priors_initialization(f_space):
    length = f_space.shape[0]
    priors = np.zeros((length,))
    # uniform assumed
    prior = 1/length
    for idx in range(length):
        priors[idx] = prior
    return priors

def likelihoods_initialization(f_space):
    length = f_space.shape[0]
    likelihoods = np.zeros((length,))
    # uniform assumed
    likelihood = 1/length
    for idx in range(length):
        likelihoods[idx] = likelihood
    return likelihoods

def get_first_posterior_for_all_positions(prior, likelihood):
    posterior = ((1-likelihood)*prior)/(1-(likelihood*prior))
    return posterior

def get_posterior_for_position_i(prior_i, likelihood_i):
    posterior_i = ((1-likelihood_i)*prior_i)/(1-(likelihood_i*prior_i))
    return posterior_i

def get_posterior_for_position_j(prior_j, likelihood_j,
                                 prior_i, likelihood_i):
    posterior_j = prior_j/(1-(likelihood_i*prior_i))
    return posterior_j

def get_arbitrary_priors(priors, true_position, distance=10):
    offset = 10
    length = priors.shape[0]
    pseudo_target_position = true_position + distance
    if pseudo_target_position > length:
        pseudo_target_position = true_position - distance
    # Get values
    values=[]
    for idx in range(length):
        offset = abs(pseudo_target_position - idx)
        offset = 1 + offset*abs(np.random.normal(0,0.0001))
        offset = 1/(np.log(offset)+100)
        values.append(offset)
    for idx in range(length):
        priors[idx] = values[idx]
    # Normalize
    priors = priors/np.sum(priors)
    return priors

print()
print("**********************************************")
print("*                                            *")
print("*        Bayesian Search Simulator           *")
print("*                                            *")
print("*              by  J.-C. Cho                 *")
print("*                                            *")
print("**********************************************")
print()

x_size = 10
space = generate_2D_space(x_size)
space = mark_true_position(space)
f_space = flatten_space(space)
true_position = np.argmax(space)

print()
print("=== SEARCH SPACE =============================")
print(space)
print("----------------------------------------------")
print("True Position:", true_position, "in flattend space")
print("==============================================")
input("Press 'Enter key' to continue")
print()

priors = priors_initialization(f_space)
likelihoods = likelihoods_initialization(f_space)

print()
print("----------------------------------------------")
print("Likelihood: Uniform Distribution")
print("Prior: Arbitray Near Uniform Distribution")
print("----------------------------------------------")
input("Press 'Enter key' to continue")
print()

priors = get_arbitrary_priors(priors,true_position, distance=10)
priors_for_presentation = priors.reshape((x_size, x_size))*100
print()
print("=== Priors ====================================")
print("Arbitrary (alomost Uniform) priors")
print("       X 100 for presentation")
print("----------------------------------------------")
print(priors_for_presentation)
print("==============================================")
input("Press 'Enter key' to continue")
print()
      
trial = 1
length = x_size*x_size
posteriors = np.zeros((length,))
for i in range(length):
    prior = priors[i]
    likelihood = likelihoods[i]
    posterior = get_first_posterior_for_all_positions(prior, likelihood)
    posteriors[i] = posterior
search_position = np.argmax(posteriors)
print("Trial #", trial, "Search Position:", search_position)
if search_position == true_position:
    print("******* SUCCESS *******")
    quit()

while search_position != true_position:
    trial = trial + 1
    # Bayesian Update
    searched_position = search_position
    priors = posteriors
    prior_i = priors[searched_position]
    likelihood_i = likelihoods[searched_position]
    # Bayesian Update
    for j in range(length):
        if j == searched_position:
            posterior = get_posterior_for_position_i(prior_i, likelihood_i)
        else:
            prior_j = priors[j]
            likelihood_j = likelihoods[j]
            posterior = get_posterior_for_position_j(prior_j, likelihood_j,
                                                     prior_i, likelihood_i)
        posteriors[j] = posterior       
    search_position = np.argmax(posteriors)
    print("Trial #", trial, "Search Position:", search_position)
    if search_position == true_position:
        print("***** SUCCESS!!! *****")
        break


