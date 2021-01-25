
import warnings
import numpy as np
import pandas as pd
import scipy.stats as st
import statsmodels as sm
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['figure.figsize'] = (16.0, 12.0)
matplotlib.style.use('ggplot')

# Create models from data
def best_fit_distribution(data, bins=200, ax=None):
    """Model data by finding best fit distribution to data"""
    # Get histogram of original data
    y, x = np.histogram(data, bins=bins, density=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0

    data = np.array(data)
    # Distributions to check
    # DISTRIBUTIONS = [        
    #     st.alpha,st.anglit,st.arcsine,st.beta,st.betaprime,st.bradford,st.burr,st.cauchy,st.chi,st.chi2,st.cosine,
    #     st.dgamma,st.dweibull,st.erlang,st.expon,st.exponnorm,st.exponweib,st.exponpow,st.f,st.fatiguelife,st.fisk,
    #     st.foldcauchy,st.foldnorm,st.genlogistic,st.genpareto,st.gennorm,st.genexpon,
    #     st.genextreme,st.gausshyper,st.gamma,st.gengamma,st.genhalflogistic,st.gilbrat,st.gompertz,st.gumbel_r,
    #     st.gumbel_l,st.halfcauchy,st.halflogistic,st.halfnorm,st.halfgennorm,st.hypsecant,st.invgamma,st.invgauss,
    #     st.invweibull,st.johnsonsb,st.johnsonsu,st.ksone,st.kstwobign,st.laplace,st.levy,st.levy_l,st.levy_stable,
    #     st.logistic,st.loggamma,st.loglaplace,st.lognorm,st.lomax,st.maxwell,st.mielke,st.nakagami,st.ncx2,st.ncf,
    #     st.nct,st.norm,st.pareto,st.pearson3,st.powerlaw,st.powerlognorm,st.powernorm,st.rdist,st.reciprocal,
    #     st.rayleigh,st.rice,st.recipinvgauss,st.semicircular,st.t,st.triang,st.truncexpon,st.truncnorm,st.tukeylambda,
    #     st.uniform,st.vonmises,st.vonmises_line,st.wald,st.weibull_min,st.weibull_max,st.wrapcauchy
    # ]
    DISTRIBUTIONS = [        
        st.alpha,st.beta,st.betaprime,st.cauchy,st.chi,st.chi2,st.erlang,st.expon,st.exponnorm,
        st.gennorm,
        st.gamma,st.gengamma,
        st.invgamma,st.invgauss,
        st.invweibull,st.laplace,
        st.logistic,st.loggamma,st.loglaplace,st.lognorm,st.lomax,st.maxwell,
        st.norm,st.pearson3,st.powerlaw,st.powerlognorm,st.powernorm,st.rdist,st.reciprocal,
        st.rayleigh,st.t,st.tukeylambda,
        st.uniform,
    ]

    DISTRIBUTIONS = [  st.lognorm,st.norm ,st.powerlognorm,st.powernorm ]
    # Best holders
    best_distribution = st.norm
    best_params = (0.0, 1.0)
    best_sse = 1 # If doing chi fit
    best_p = 1
    # Estimate distribution parameters from data
    for distribution in DISTRIBUTIONS:
        
        # Try to fit the distribution
        try:
            # Ignore warnings from data that can't be fit
            with warnings.catch_warnings():
                #warnings.filterwarnings('ignore')
                print("TRY: "+str(distribution))

                # fit dist to data
                params = distribution.fit(data)


                # Separate parts of parameters
                arg = params[:-2]
                loc = params[-2]
                scale = params[-1]

                # Calculate fitted PDF and error with fit in distribution
                pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                sse = np.sum(np.power(y - pdf, 2.0))

                # sub p-value in for sse
                observed_values , bin_edges = np.histogram(data, bins=bins, density = True)
                cdf = distribution.pdf(bin_edges, loc=loc, scale=scale, *arg)
                expected_values = len(data) * np.diff(cdf)
                sse , p = st.chisquare(observed_values, expected_values, ddof=len(params))

                # if axis pass in add to plot
                try:
                    if ax:
                        pd.Series(pdf, x).plot(ax=ax)
                    
                except Exception:
                    pass

                # identify if this distribution is better
                #if best_sse > sse > 0:
                if best_sse < sse : # if useing pvalue
                    best_distribution = distribution
                    best_params = params
                    best_sse = sse
                    best_p = p

        except Exception:
            print(str(distribution) + " failed. ")
            pass

    return (best_distribution.name, best_params, best_sse, best_p)

def make_pdf(dist, params, size=10000):
    """Generate distributions's Probability Distribution Function """

    # Separate parts of parameters
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]

    # Get sane start and end points of distribution
    start = dist.ppf(0.01, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.01, loc=loc, scale=scale)
    end = dist.ppf(0.99, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.99, loc=loc, scale=scale)

    # Build PDF and turn into pandas Series
    x = np.linspace(start, end, size)
    y = dist.pdf(x, loc=loc, scale=scale, *arg)
    pdf = pd.Series(y, x)

    return pdf
###################################################################################
###################################################################################
Stream_people = 140;
Sunset_people = 110;

stream_volume = pd.read_csv('C:/Users/paul/Documents/GitHub/HPWH-Sizing-Tool---Research/metered_data/stream_volume.csv')
sunset_volume = pd.read_csv('C:/Users/paul/Documents/GitHub/HPWH-Sizing-Tool---Research/metered_data/sunset_volume.csv')

stream_volume['valupp']= stream_volume['value'] / Stream_people
sunset_volume['valupp']= sunset_volume['value'] / Sunset_people

df = stream_volume.groupby('dates').agg(gpdpp = pd.NamedAgg(column='valupp',aggfunc=sum)).reset_index()
#df = sunset_volume.groupby('dates').agg(gpdpp = pd.NamedAgg(column='valupp',aggfunc=sum)).reset_index()

###################################################################################
# Load data from statsmodels datasets
data = df.drop(columns=['dates'])

# Plot for comparison
plt.figure(figsize=(12,8))
ax = data.plot(kind='hist', bins=50, density=True, alpha=0.5)
# Save plot limits
dataYLim = ax.get_ylim()

# Find best fit distribution
best_fit_name, best_fit_params, best_sse, best_p = best_fit_distribution(data, 200, ax)
best_dist = getattr(st, best_fit_name)

# Update plots
ax.set_ylim(dataYLim)
ax.set_xlabel(u'GPDPP')
ax.set_ylabel('Frequency')
plt.show()

# Make PDF with best params 
pdf = make_pdf(best_dist, best_fit_params)


# Display
plt.figure(figsize=(12,8))
ax = pdf.plot(lw=2, label='PDF', legend=True)
data.plot(kind='hist', bins=50, density=True, alpha=0.5, label='Data', legend=False, ax=ax)

param_names = (best_dist.shapes + ', loc, scale').split(', ') if best_dist.shapes else ['loc', 'scale']
param_str = ', '.join(['{}={:0.6f}'.format(k,v) for k,v in zip(param_names, best_fit_params)])
dist_str = '{}({})'.format(best_fit_name, param_str)

ax.set_title(u'Best fit distribution \n' + dist_str)
ax.set_xlabel(u'GPDPP')
ax.set_ylabel('Frequency')

print("p-value: %0.6f " % best_p)