from abc import ABC, abstractmethod
import numpy as np
from scipy.optimize import minimize


class AbstractPortfolioOptimization(ABC):
    
    def __init__(self, n_assets):
        self.solution = None
        self.n_assets = n_assets
    
    @abstractmethod
    def objective_function(self, weights, mu, cov, *args, **kwargs):
        raise NotImplementedError("should implement in the derived class")

    @abstractmethod
    def constraints(self, *args, **kwargs):
        raise NotImplementedError("should implement in the derived class")
    
    @abstractmethod
    def bounds(self, *args, **kwargs):
        return tuple((0, 1) for _ in range(self.n_assets))

    def _optimize(self, mu, cov, *args, **kwargs):
        self.solution = minimize(
            lambda weights: self.objective_function(weights, mu, cov, *args, **kwargs), 
            self.initial_guess(), 
            method='SLSQP', 
            bounds=self.bounds(*args, **kwargs), 
            constraints=self.constraints(*args, **kwargs)
            )

    def get_optimal_weights(self):
        if self.solution is not None:
            return self.solution.x
        else:
            return "No solution found yet. Please run the optimize method first."

    def initial_guess(self):
        init = np.random.uniform(0, 1, size=self.n_assets)
        return init / np.sum(init)

    def __call__(self, mu, cov, *args, **kwargs):
        self._optimize(mu, cov, *args, **kwargs)
        return self.solution.x


class MinVarPortfolio(AbstractPortfolioOptimization):
    
    def objective_function(self, weights, mu, cov, *args, **kwargs):
        portfolio_mean = weights.T @ mu
        portfolio_variance = weights.T @ cov @ weights
        max_obj = - portfolio_variance
        return - max_obj

    def constraints(self, *args, **kwargs):
        return ({'type': 'eq', 
                 'fun': lambda weights: np.sum(weights) - 1})
    
    def bounds(self, *args, **kwargs):
        return tuple((0, 1) for _ in range(self.n_assets))
    

class MeanVarPortfolio(AbstractPortfolioOptimization):

    def objective_function(self, weights, mu, cov, *args, **kwargs):
        portfolio_mean = weights.T @ mu
        portfolio_variance = weights.T @ cov @ weights
        max_obj = - portfolio_variance
        return - max_obj

    def constraints(self, *args, **kwargs):
        target_return = kwargs["target_return"]
        mean_return = kwargs["mean_return"]
        return ({'type': 'eq', 
                 'fun': lambda weights: np.sum(weights) - 1},
                {'type': 'eq',
                 'fun': lambda weights: weights.T @ mean_return - target_return})
    
    def bounds(self, *args, **kwargs):
        return tuple((0, 1) for _ in range(self.n_assets))
    

class QuadUtilityPortfolio(AbstractPortfolioOptimization):

    def objective_function(self, weights, mu, cov, *args, **kwargs):
        assert "alpha" in kwargs
        alpha = kwargs["alpha"]
        portfolio_mean = weights.T @ mu
        portfolio_variance = weights.T @ cov @ weights
        max_obj =  portfolio_mean - 0.5 * alpha * portfolio_variance
        return - max_obj

    def constraints(self, *args, **kwargs):
        return ({'type': 'eq', 
                 'fun': lambda weights: np.sum(weights) - 1})
    
    def bounds(self, *args, **kwargs):
        return tuple((0, 1) for _ in range(self.n_assets))


class AnalyticMinVarPortfolio(AbstractPortfolioOptimization):

    def objective_function(self, weights, mu, cov, *args, **kwargs):
        pass

    def constraints(self, *args, **kwargs):
        pass

    def bounds(self, *args, **kwargs):
        pass

    def __call__(self, mu, cov, *args, **kwargs):
        iota = np.repeat(1, self.n_assets)
        try:
            inv_cov = np.linalg.inv(cov)
            target_position = (inv_cov @ iota) / (iota.T @ inv_cov @ iota)

        except np.linalg.LinAlgError:
            print("uninvertiable covariance matrix detected!")
            target_position = np.repeat(1/self.n_assets, self.n_assets)

        return target_position


class AnalyticMeanVarPortfolio(AbstractPortfolioOptimization):

    def objective_function(self, weights, mu, cov, *args, **kwargs):
        pass

    def constraints(self, *args, **kwargs):
        pass

    def bounds(self, *args, **kwargs):
        pass

    def __call__(self, mu, cov, *args, **kwargs):
        mean_return = kwargs["mean_return"]
        target_return = kwargs["target_return"]
        iota = np.repeat(1, self.n_assets)
        try:
            inv_cov = np.linalg.inv(cov)
            A = mu.T @ inv_cov @ mu
            B = iota.T @ inv_cov @ mu
            C = mu.T @ inv_cov @ iota
            D = iota.T @ inv_cov @ iota

            y = D / (A*D - B*C) * inv_cov @ mu - C / (A*D - B*C) * inv_cov @ iota
            z = A / (A*D - B*C) * inv_cov @ iota - B / (A*D - B*C) * inv_cov @ mu
            target_position = target_return * y + z
        except np.linalg.LinAlgError:
            print("uninvertiable covariance matrix detected!")
            target_position = np.repeat(1/len(self.n_assets), self.n_assets)

        return target_position
    

class AnalyticQuadUtilityPortfolio(AbstractPortfolioOptimization):

    def objective_function(self, weights, mu, cov, *args, **kwargs):
        pass

    def constraints(self, *args, **kwargs):
        pass

    def bounds(self, *args, **kwargs):
        pass

    def __call__(self, mu, cov, *args, **kwargs):
        alpha = kwargs["alpha"]
        iota = np.repeat(1, self.n_assets)

        try:
            inv_cov = np.linalg.inv(cov)
            gamma = ( iota.T @ inv_cov @ mu) / (iota.T @ inv_cov @ iota)
            target_position = ( inv_cov @ iota) / (iota.T @ inv_cov @ iota) + (1/alpha) * inv_cov @ (mu - gamma * iota)

        except np.linalg.LinAlgError:
            print("uninvertiable covariance matrix detected!")
            target_position = np.repeat(1/len(self.n_assets), self.n_assets)
        
        return target_position
    
